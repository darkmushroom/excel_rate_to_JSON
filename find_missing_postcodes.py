# Find all missing postcodes in input string within a range
def counter(input, start, end, output_padding):

  # format text input into list of ints
  input = input.strip().split(',')
  input = [int(element) for element in input]
  input.sort()

  # list of all possible postcodes for comparison
  all_possible_postcodes = []
  for i in range (start, end+1):
    all_possible_postcodes.append(i)

  # remove postcodes in the input from our mega list, apply padding, and reconstitute them into an output string
  output = [str(element) for element in (set(all_possible_postcodes) - set(input))]
  output = [element.zfill(output_padding) for element in output]
  output = ', '.join(output)
  return output
