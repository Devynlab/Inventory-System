import base64
from io import BytesIO

import matplotlib.pyplot as plt


def get_graph():
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_png = buffer.getvalue()
  graph = base64.b64encode(image_png)
  graph = graph.decode('utf-8')
  buffer.close()
  return graph

def get_plot(x, y):
  plt.switch_backend('AGG')
  plt.figure(figsize=(6, 4))
  plt.title('Sales of Items')
  plt.plot(x, y)
  plt.ylabel('Amount in (Ksh)')
  plt.tight_layout()
  return get_graph()
