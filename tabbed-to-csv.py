import csv
import os
import sys
import click
import time

__version__ = '1.0'

def write_out(msg):
  if write_out.verbose:
    print(msg)

class TabToCsv:
  def __init__(self, path, output):
    self.path = path
    self.output = output
    self.columnNames = None
    self.data = []
    self.rows = 0
    self.columns = 0
  
  def process_file(self):
    # _axgt = csv.reader(open('./data/axon_data/axontextfile_tab_delimited.axgt', "r"), delimiter='\t')
    # _csv = csv.writer(open('./data/exported/axondata.csv', 'w'))
    #
    # _csv.writerows(_axgt)
    with open(self.path, encoding="utf8") as csvfile:
      rdr = csv.reader(csvfile, delimiter='\t')
      self.columnNames = [name for name in next(rdr)]
      cols = len(self.columnNames)
      for row in rdr:
        self.rows = self.rows + 1
        self.data.append(row)
        for col in range(cols):
          self.columns = self.columns + 1
      writer = csv.writer(open(self.output, 'w'))
      writer.writerows(rdr)

@click.command()
@click.option("--file", "-f",
              type=click.Path(exists=True),
              help="A file to convert into csv.",
              multiple=True
              )
@click.option("--output", "-o",
              type=click.Path(),
              help="The output csv file path",
              default=os.path.basename(os.getcwd()) + ".csv"
              )
@click.option("--verbose", "-v",
              is_flag=True,
              help="Verbose logging",
              default=False
              )
def start(file, output, verbose):
  """
  Script
  """
  write_out.verbose = verbose
  files = list(file)
  if not sys.stdin.isatty():
    files.extend(list(sys.stdin))
  if not files:
    write_out("No files were specified. Exiting.")
    return
  write_out("Output file: " + output)
  with click.progressbar(files) as _files:
    actual = files if verbose else _files
    for file in actual:
      try:
        file = file.strip()
        write_out("Processing " + file)
        info = TabToCsv(file, output)
        info.process_file()
      except Exception as exc:
        print("\n Error: \n")
        print(exc)

if __name__ == "__main__":
  start()
