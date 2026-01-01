from sqlalchemy import create_engine
import os
abs_path=os.path.abspath(__file__)
dir_name=os.path.dirname(abs_path)
engine = create_engine(f"sqlite:///{dir_name}/sample.db")
