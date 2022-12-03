# Import the necessary libraries
import hashlib
import json
import socket
from typing import Dict, List

# Define the data structure for a microblog post
class MicroblogPost:
  def __init__(self, username: str, content: str):
    self.username = username
    self.content = content
    self.timestamp = time.time()
  
  # Generate a unique ID for the post
  def generate_id(self) -> str:
    # Hash the post content and the timestamp
    post_data = (self.content + str(self.timestamp)).encode()
    hashed_data = hashlib.sha256(post_data).hexdigest()
    # Return the hashed data as the post ID
    return hashed_data

    
# Define the P2P network node
class MicroblogNode:
  def __init__(self, node_id: str, username: str, host: str, port: int):
    self.node_id = node_id
    self.username = username
    self.host = host
    self.port = port
    self.posts = [] # List of microblog posts
    self.peers = [] # List of peer nodes
    self.socket = None # Socket for communicating with peer nodes
  
  # Open the socket and listen for incoming connections
  def listen(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.host, self.port))
    self.socket.listen()
    # Accept incoming connections
    while True:
      connection, address = self.socket.accept()
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
  def add_peer(self, peer: 'MicroblogNode'):
    self.peers.append(peer)
  
  # Connect to a peer node and add it to the network
  def connect_to_peer(self, peer: 'MicroblogNode'):
    # Connect to the peer node's socket
    peer_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer.host, peer.port))
    # Add the peer node to the network
    self.add_peer(peer)
  
  # Broadcast a microblog post to all connected peer nodes
  def broadcast_post(self, post: MicroblogPost):
    # Serialize the post data
    post_data = json.dumps(post.__dict__)
    # Loop over the connected peer nodes
    for peer in self.peers:
      # Send the post data to the peer node
      peer.sendall(post_data)

# Define the P2P network
class MicroblogNetwork:
  def __init__(self):
    self.nodes = {} # Dictionary of nodes in the network
  
  # Add a new node to the network
  def add_node(self, node: MicroblogNode):
    self.nodes[node.node_id] = node
  
  # Get a list of all nodes in the network
  def get_nodes(self) -> List[MicroblogNode]:
    return self.nodes.values()
  
  # Broadcast a microblog post to all nodes in the network
  def broadcast_post(self, post: MicroblogPost):
    for node in self.nodes.values():
      node.broadcast_post(post)

# Define the main function
def main():
  # Create a new P2P network
  network = MicroblogNetwork()

  # Create a new node and add it to the network
  node1 = MicroblogNode('node1', 'Alice', 'localhost', 8080)
  network.add_node(node1)
  # Start listening for incoming connections on the node
  node1.listen()

  # Create another node and add it to the network
  node2 = MicroblogNode('node2', 'Bob', 'localhost', 8081)
  network.add_node(node2)
  # Start listening for incoming connections on the node
  node2.listen()

  # Connect node2 to node1
  node2.connect_to_peer(node1)

  # Create a new microblog post and broadcast it to the network
  post = MicroblogPost('Alice', 'Hello, world!')
  network.broadcast_post(post)

  # Get the posts from node1
  posts = node1.get_posts()
  # Print the posts
  for post in posts:
    print(f'{post.username}: {post.content}')

# Run the main function
if __name__ == '__main__':
  main()
