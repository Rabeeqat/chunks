from time import time
import matplotlib.pyplot as plt

class Entry:
  def __init__(self, timestamp):
      self.timestamp = timestamp

class Chunk:
  def __init__(self):
      self.entries = []
      for _ in range(10):
          self.addEntry()

  def addEntry(self):
    self.entries.append(time())

  def isFull(self):
    return len(self.entries) >= 10

class portInfo:
  def __init__(self,port_id):
    self.port_id = port_id
    self.chuncksData = []
    self.currentChunck=Chunk()
    self.chuncksData.append(self.currentChunck)
    
class chunkManager:
  def __init__(self,noOfPorts,initialChunks):
    self.globalQueue = []
    self.noOfPorts=noOfPorts
    for _ in range(initialChunks):
      chunk=Chunk()
      self.globalQueue.append(chunk)
    self.port_infos = {port_id: portInfo(port_id) for port_id in range(noOfPorts)}
    self.tracker = PortTracker(noOfPorts)

  def addEntries(self,port_id):
    if self.port_infos[port_id].currentChunck.isFull():
      self.port_infos[port_id].currentChunck=Chunk()
      self.port_infos[port_id].chuncksData.append(self.port_infos[port_id].currentChunck)
    self.port_infos[port_id].chuncksData[len(self.port_infos[port_id].chuncksData)-1].addEntry()
    self.port_infos[port_id].currentChunck=self.port_infos[port_id].chuncksData[-1]

  def add_event(self, port_id):
    if self.port_infos[port_id].currentChunck:
      lastChunk=self.port_infos[port_id].chuncksData[-1]
      firstChunk=self.globalQueue[0]
      #print(length,"\n\nIN\n")
      for i in range (self.noOfPorts):
        chunks=self.port_infos[i].chuncksData
        if firstChunk in chunks:
          if len(chunks) <= 1:
            return
          self.port_infos[i].chuncksData.remove(firstChunk)
      self.globalQueue.pop(0)
      self.globalQueue.append(lastChunk)
      self.port_infos[port_id].chuncksData.append(firstChunk)
      self.port_infos[port_id].currentChunck=firstChunk
      self.tracker.update(port_id, len(self.port_infos[port_id].currentChunck.entries))
      print("LENGTH: ",len(self.port_infos[port_id].currentChunck.entries))

  def display(self):
    #for i in range (len(self.globalQueue)):
    print("GLOBAL_CHUNKS")
    print("GLOBAL",0," :",self.globalQueue[0].entries)
    #print("Global",9," :",self.globalQueue[9].entries)
    #print("\n")
      
    for i in range (self.noOfPorts):
      chunks=self.port_infos[i].chuncksData
      print("\nCHUNKS AT PORT",i)
      for j in range (len(chunks)):
        print("Chunk",j," :",chunks[j].entries)
          
class PortTracker:
  def __init__(self, num_ports):
      self.num_ports = num_ports
      self.data = {i: {'time': [], 'num_chunks': []} for i in range(num_ports)}

  def update(self, port_id, num_chunks):
      current_time = time()
      self.data[port_id]['time'].append(current_time)
      self.data[port_id]['num_chunks'].append(num_chunks)

  def plot(self):
      plt.figure(figsize=(12, 8))
      for port_id in range(self.num_ports):
          plt.plot(self.data[port_id]['time'], self.data[port_id]['num_chunks'], label=f'Port {port_id}')
      plt.xlabel('Time')
      plt.ylabel('Number of Chunks')
      plt.title('Chunk Usage Over Time for Ports')
      plt.legend()
      plt.grid(True)
      plt.show()


def main():
  num_ports = 2
  initial_chunks = 1
  manager = chunkManager(num_ports, initial_chunks)
  print("\n\n**Chunks at Start**\n")
  manager.display()
  port_id=1
  manager.add_event(port_id)
  #manager.tracker.plot()
  print("\n\n**After adding one chunk from Global Queue to Port1**\n")
  manager.display()
  manager.add_event(0)
  #manager.tracker.plot()
  print("\n\n**After adding one chunk from Global Queue to Port0**\n")
  #manager.addEntries(1)
  manager.display()
  manager.tracker.plot()
if __name__ == "__main__":
  main()
