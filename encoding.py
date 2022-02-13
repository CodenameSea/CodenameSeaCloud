chars = "abcdefghijklmnopqrstuvwxyz0123456789+-. _"
def encode(text):
  encoded = ""
  for letter in text:
    encoded = encoded + str(chars.find(letter) + 11)
  return encoded
def decode(text):
  decoded = ""
  text = str(text)
  y = 0
  for i in range(0, len(text)//2):
    order = int(text[y] + text[y+1]) - 11
    decoded = decoded + chars[order]
    y += 2
  return decoded