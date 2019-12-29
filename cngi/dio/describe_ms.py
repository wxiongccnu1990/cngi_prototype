#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


#############################################
def describe_ms(infile):
  """
   Summarize the contents of a zarr format MS directory on disk

   Parameters
   ----------
   infile : str
       input filename of zarr MS
   
   Returns
   -------
   Pandas Dataframe
       Summary information
   """
  import os
  import numpy as np
  import pandas as pd
  import pyarrow.parquet as pq
  
  infile = os.path.expanduser(infile)  # does nothing if $HOME is unknown
  if ddis == None:
    try:
      ddis = list(np.array(os.listdir(infile), dtype=int))
    except ValueError:
      # relative paths include basename in listdir
      ddis = list(np.array(os.listdir(infile)[1:], dtype=int))
  elif type(ddis) != list:
    ddis = [ddis]
  
  summary = pd.DataFrame([])
  for ddi in ddis:
    dpath = os.path.join(infile, str(ddi))
    chunks = os.listdir(dpath)
    dsize = np.sum([os.path.getsize(os.path.join(dpath, ff)) for ff in chunks]) / 1024 ** 3
    pqf = pq.ParquetFile(os.path.join(dpath, chunks[0]))
    sdf = [{'ddi': ddi, 'chunks': len(chunks), 'size_GB': np.around(dsize, 2),
            'row_count_estimate': pqf.metadata.num_rows * len(chunks),
            'col_count': pqf.metadata.num_columns, 'col_names': pqf.schema.names}]
    summary = pd.concat([summary, pd.DataFrame(sdf)], axis=0, sort=False)
  
  summary = summary.reset_index().drop(columns=['index'])
  return summary