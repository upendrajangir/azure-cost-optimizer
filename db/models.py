from sqlalchemy import Table, Column, Integer, String
from .connection_manager import Base


class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_name = Column(String)
    resource_type = Column(String)
    current_sku = Column(String)
    cpu_weight_avg = Column(Integer)
    cpu_weight_peak = Column(Integer)
    cpu_weight_peak_duration = Column(Integer)
    cpu_weight_bottom = Column(Integer)
    memory_weight_avg = Column(Integer)
    memory_weight_peak = Column(Integer)
    memory_weight_peak_duration = Column(Integer)
    memory_weight_bottom = Column(Integer)
    storage_weight_avg = Column(Integer)
    other_weight_avg = Column(Integer)
    other_weight_peak = Column(Integer)
    current_weightage = Column(Integer)
    suggested_sku = Column(String)
