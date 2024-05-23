class Node_List:
    def init(self,key,value):
        self.key = key 
        self.value = value 
        self.prev = None
        self.next = None
    
class linked_list:
    def init(self):
        self.head = Node_List(0,0)
        self.tail = Node_List(0,0)
        self.head.next = self.tail #ヘッドの次をテイルに設定
        self.head.prev = self.head #テイルの前をヘッドに設定
    
    
    def add(self, node: Node_List) -> None:
        node.prev = self.head #新しいノードの前をヘッドに設定
        node.next = self.head.next #新しいノードの次をヘッドの次に設定
        self.head.next.prev = node #元のヘッドの次のノードの前を新しいノードに設定
        self.head.prev = node #ヘッドの次を新しいノードに設定
    
    def remove(self, node: Node_List) -> None:
        node.prev.next = node.next #削除するノードの前のノードの次を削除するノードの次に設定
        node.next.prev = node.prev #削除するノードの次のノードの前を削除するノードの前に設定

    def move_to_head(self, node: Node_List) -> None:
        self.remove(node)
        self.add(node)