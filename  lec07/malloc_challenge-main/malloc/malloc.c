//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);
size_t BUFFER_SIZE = 4096;

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;
  my_metadata_t dummy;
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

void my_add_to_free_list(my_metadata_t *metadata) {
  // assert(!metadata->next);
  // metadata->next = my_heap.free_head;
  // my_heap.free_head = metadata;
  my_metadata_t *current = my_heap.free_head;
  my_metadata_t *prev = NULL;

  // metadataがcurrentよりも前の位置を指している間
  while (current != &my_heap.dummy && current < metadata)
  {
      prev = current;
      current = current->next;
  }

  metadata->next = current;
  if (prev) {
    prev->next = metadata;
  } else {
    my_heap.free_head = metadata;
  }
}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  my_heap.free_head = &my_heap.dummy;
  my_heap.dummy.size = 0;
  my_heap.dummy.next = NULL;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().

void *my_malloc(size_t size) {
  my_metadata_t *metadata = my_heap.free_head;
  my_metadata_t *prev = NULL;
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_fit_prev = NULL;
  // First-fit: Find the first free slot the object fits.
  // TODO: Update this logic to Best-fit!

  // while (metadata && metadata->size < size) {
  //   prev = metadata;
  //   metadata = metadata->next;
  // }

//Best_fit十分な大きさの空き領域のうち最も小さいもの
  while (metadata) {
    if (metadata->size >= size) {
      if (!best_fit || metadata->size < best_fit->size) {
        best_fit = metadata;
        best_fit_prev = prev;
      }
    }
    prev = metadata;
    metadata = metadata->next;
  }

  metadata = best_fit;
  prev = best_fit_prev;
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);

  my_metadata_t *free = my_heap.free_head;
  my_metadata_t *prev = NULL;
  //最後のフリースロットを探す
  while (free && free->next != &my_heap.dummy){
    prev = free;
    free = free->next;}
  // フリースロットのサイズを計算
  size_t size = free->size + (sizeof(my_metadata_t));
  // 4KBの空き
  if(size % BUFFER_SIZE == 0){
      // Free Listの一番はじめ
      if (my_heap.free_head == free){
          my_heap.free_head = free->next;
      }
      else{
          prev->next = free->next;}
      munmap_to_system(free, size);
  }
  // 4KB以上の空きの時
  else if (free->size > BUFFER_SIZE){
      size_t n = free->size / BUFFER_SIZE;
      my_metadata_t *begin = (my_metadata_t *)((char *)free + size - BUFFER_SIZE * n);
      // 末尾にデータが入っていたら
      if ((uintptr_t)(begin) % 4096 != 0)
          return;
      free->size -= BUFFER_SIZE * n;
      begin->size = BUFFER_SIZE * n - sizeof(my_metadata_t);
      munmap_to_system(begin, BUFFER_SIZE * n);
  }
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
