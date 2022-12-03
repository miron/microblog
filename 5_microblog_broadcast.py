import json
from typing import List
import socket
import uuid

class MicroblogPost:
  def __init__(self, username: str, content: str):
    self.username = username
    self.content = content

class MicroblogNode:
  def __init__(self, username: str, ip: str, port: int):
    self.node_id = str(uuid.uuid1()) # Generate a unique node ID
    self.username = username
    self.ip = ip
    self.port = port
    self.posts = [] # List of microblog posts
    self.peers = [] # List of peer nodes
  
  # Open the socket and listen for incoming connections
  def listen(self):
    # Create a new socket
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((self.ip, self.port))
    socket.listen()
    # Accept incoming connections
    while True:
      connection, address = socket.accept()
      # Receive data from the incoming connection
      data = connection.recv(1024)
      # Deserialize the data
      data = json.loads(data)
      # Create a new microblog post from the received data
      post = MicroblogPost(data['username'], data['content'])
      # Add the post to the node's list of posts
      self.add_post(post)

  # Add a new microblog post to the node
  def add_post(self, post: MicroblogPost):
    self.posts.append(post)
  
  # Get all microblog posts from the node
  def get_posts(self) -> List[MicroblogPost]:
    return self.posts
  
  # Add a new peer node to the network
  def add_peer(self, peer: MicroblogNode):
    self.peers.append(peer)
  
  # Connect to a peer node and add it to the network
  def connect_to_peer(self, peer: MicroblogNode):
    # Connect to the peer node's socket
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer.ip, peer.port))
    # Add the peer node to the network
    self.add_peer(peer)

  # Broadcast a microblog post to all connected peer nodes
  def broadcast_post(self, post: MicroblogPost):
    # Serialize the post data
    post_data = json.dumps(post.__dict__)
    # Loop over the connected peer nodes
    for peer in self.peers:
      # Send the post data to the peer node
      peer.socket.send(post_data)
  
  # Broadcast the node's IP address to all connected peer nodes
  def broadcast_ip(self):
    # Serialize the IP address
    ip_data = json.dumps(self.ip)
    # Loop over the connected peer nodes
    for peer in self.peers:
      # Send the IP address to the peer node
      peer.socket.send(ip_data)

class MicroblogNetwork:
  def __init__(self):
    self.nodes = [] # List of nodes in the network
  
  # Add a new node to the network
  def add_node(self, node: MicroblogNode):
    self.nodes.append(node)
  
  # Broadcast a microblog post to all nodes in the network
  def broadcast_post(self, post: MicroblogPost):
    for node in self.nodes:
      node.broadcast_post(post)


def main():
  network = MicroblogNetwork()

  host = socket.gethostbyname(socket.gethostname())

  node1 = MicroblogNode('Alice', host, 8080)
  network.add_node(node1)
  node1.listen()

  node2 = MicroblogNode('Bob', host, 8081)
  network.add_node(node2)
  node2.listen()

  node2.connect_to_peer(node1)

  # Broadcast the node IP addresses
  node1.broadcast_ip()
  node2.broadcast_ip()

  post = MicroblogPost('Alice', 'Hello, world!')
  node1.broadcast_post(post)

  posts = node2.get_posts()
  print(posts)

if __name__ == '__main__':
  main()
