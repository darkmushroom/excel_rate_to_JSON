# assumes all elements in the list are the same initial size
def reduce(postcode_list):
  parse = postcode_list.split(',')
  parse = [s.strip() for s in parse]
  parse.sort()

  output = reduce_it(parse)
  return ', '.join(output)

def reduce_it(parse, size = -1):
  # this is our first iteration
  if size == -1:
    size = len(parse[0])
  
  # cannot reduce any further
  if size == 0:
    return parse

  length = len(parse)
  output = []

  i = 0
  # loop through each element in parse
  while i < length:
    is_contiguous = False
    
    # if the last character is a 0, we may be able to reduce
    if parse[i][-1:] == '0' and i+9 <= length:
      # start here and loop through the next 9 items to see if they are contiguous and correctly sized
      for j in range(0, 9):
        if parse[i + j][-1:] == str(j) and not len(parse[i + j]) > size:
          is_contiguous = True
        else:
          is_contiguous = False
          break
    
    if is_contiguous:
      output.append(parse[i][:-1])
      i += 9
    else:
      output.append(parse[i])
    
    i += 1

  return reduce_it(output, size-1)
