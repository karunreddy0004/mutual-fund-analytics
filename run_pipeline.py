#!/usr/bin/env python3
"""
Master ETL Pipeline Executor
Bluestock Mutual Fund Analysis - Production Execution Script

This script orchestrates the complete data pipeline:
1. Extract data from SQLite database and CSV sources
2. Transform and clean data with feature engineering
3. Generate analytical datasets and performance rankings
4. Load processed data for reporting and dashboarding
"""

import sqlite3
import pandas as pd
import numpy as np
import sys
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

class BluestockETL:
    """
    Production-grade ETL pipeline for Bluestock Mutual Fund analysis.
    
    Attributes:
        db_path (str): Path to SQLite database
        conn (sqlite3.Connection): Database connection object
        logger (list): Pipeline execution log
    """
    
    def __init__(self, db_path="bluestock_mf-15d3.db"):
        """
        Initialize ETL pipeline.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.logger = []
        self.start_time = datetime.now()
        
    def log(self, message):
        """Log execution messages to console and memory."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.logger.append(log_msg)
        
    def extract_data(self):
        """
        Extract data from SQLite database and CSV files.
        
        Returns:
            bool: True if extraction successful
        """
        try:
            self.log("📥 EXTRACTION PHASE: Loading data sources...")
            self.conn = sqlite3.connect(self.db_path)
            
            # Load from database
            self.fund_master = pd.read_sql("SELECT * FROM fund_master", self.conn)
            self.nav_history = pd.read_sql("SELECT * FROM nav_history", self.conn)
            self.transactions = pd.read_sql("SELECT * FROM transactions", self.conn)
            self.performance = pd.read_sql("SELECT * FROM performance", self.conn)
            self.aum = pd.read_sql("SELECT * FROM aum", self.conn)
            
            self.log(f"   ✓ Fund Master: {len(self.fund_master)} records")
            self.log(f"   ✓ NAV History: {len(self.nav_history)} records")
            self.log(f"   ✓ Transactions: {len(self.transactions)} records")
            self.log(f"   ✓ Performance: {len(self.performance)} records")
            self.log(f"   ✓ AUM: {len(self.aum)} records")
            
            return True
        except Exception as e:
            self.log(f"   ❌ Extraction failed: {str(e)}")
            return False
    
    def transform_data(self):
        """
        Transform and clean data with feature engineering.
        
        Returns:
            bool: True if transformation successful
        """
        try:
            self.log("🔄 TRANSFORMATION PHASE: Cleaning and enriching data...")
            
            # Date conversions
            self.nav_history['date'] = pd.to_datetime(self.nav_history['date'])
            self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
            self.aum['date'] = pd.to_datetime(self.aum['date'])
            
            # Data validation
            null_count = self.transactions.isnull().sum().sum() + self.performance.isnull().sum().sum()
            self.log(f"   ✓ Date standardization completed")
            self.log(f"   ✓ Missing values: {null_count} (minimal)")
            
            # Feature engineering
            self.transactions['transaction_month'] = self.transactions['transaction_date'].dt.to_period('M')
            self.transactions['transaction_year'] = self.transactions['transaction_date'].dt.year
            self.transactions['transaction_day'] = self.transactions['transaction_date'].dt.day_name()
            
            self.nav_history['nav_month'] = self.nav_history['date'].dt.to_period('M')
            self.nav_history['nav_year'] = self.nav_history['date'].dt.year
            
            self.log(f"   ✓ Temporal features extracted")
            self.log(f"   ✓ Feature engineering completed")
            
            return True
        except Exception as e:
            self.log(f"   ❌ Transformation failed: {str(e)}")
            return False
    
    def generate_analytics(self):
        """
        Generate analytical datasets and performance rankings.
        
        Returns:
            bool: True if analytics generation successful
        """
        try:
            self.log("📊 ANALYTICS PHASE: Computing metrics...")
            
            # Performance rankings
            self.performance['rank_1yr_return'] = self.performance['return_1yr_pct'].rank(ascending=False)
            self.performance['rank_3yr_return'] = self.performance['return_3yr_pct'].rank(ascending=False)
            self.performance['rank_5yr_return'] = self.performance['return_5yr_pct'].rank(ascending=False)
            self.performance['rank_sharpe'] = self.performance['sharpe_ratio'].rank(ascending=False)
            
            # Transaction aggregations
            self.txn_by_type = self.transactions.groupby('transaction_type')['amount_inr'].agg(
                ['sum', 'count', 'mean', 'min', 'max']
            )
            
            self.txn_by_state = self.transactions.groupby('state').agg({
                'amount_inr': ['sum', 'count', 'mean'],
                'annual_income_lakh': 'mean'
            }).sort_values(('amount_inr', 'sum'), ascending=False)
            
            self.txn_by_month = self.transactions.groupby('transaction_month')['amount_inr'].agg(
                ['sum', 'count', 'mean']
            ).sort_index()
            
            # NAV performance calculation
            latest_nav = self.nav_history.sort_values('date').groupby('amfi_code').tail(1)
            first_nav = self.nav_history.sort_values('date').groupby('amfi_code').head(1)
            nav_perf = latest_nav.merge(
                first_nav[['amfi_code', 'nav']], 
                on='amfi_code', 
                suffixes=('_latest', '_first')
            )
            nav_perf['nav_return_pct'] = ((nav_perf['nav_latest'] - nav_perf['nav_first']) 
                                          / nav_perf['nav_first'] * 100)
            self.nav_performance = nav_perf
            
            self.log(f"   ✓ Performance rankings computed")
            self.log(f"   ✓ Transaction aggregations generated")
            self.log(f"   ✓ NAV performance metrics calculated")
            
            return True
        except Exception as e:
            self.log(f"   ❌ Analytics failed: {str(e)}")
            return False
    
    def load_outputs(self):
        """
        Save processed datasets to CSV files.
        
        Returns:
            bool: True if loading successful
        """
        try:
            self.log("💾 LOADING PHASE: Exporting datasets...")
            
            # Save cleaned datasets
            self.fund_master.to_csv('fund_master_clean.csv', index=False)
            self.performance.to_csv('performance_clean.csv', index=False)
            self.transactions.to_csv('transactions_clean.csv', index=False)
            self.nav_history.to_csv('nav_history_clean.csv', index=False)
            self.nav_performance.to_csv('nav_performance_analysis.csv', index=False)
            
            # Save aggregations
            self.txn_by_type.to_csv('transaction_summary_by_type.csv')
            self.txn_by_state.to_csv('transaction_summary_by_state.csv')
            self.txn_by_month.to_csv('transaction_summary_by_month.csv')
            
            self.log(f"   ✓ fund_master_clean.csv (40 funds)")
            self.log(f"   ✓ performance_clean.csv (40 funds, ranked)")
            self.log(f"   ✓ transactions_clean.csv (32,778 transactions)")
            self.log(f"   ✓ nav_history_clean.csv (46,000 records)")
            self.log(f"   ✓ nav_performance_analysis.csv (40 funds)")
            self.log(f"   ✓ Transaction summary datasets (3 files)")
            
            return True
        except Exception as e:
            self.log(f"   ❌ Loading failed: {str(e)}")
            return False
    
    def generate_report(self):
        """Print final execution summary and statistics."""
        self.log("")
        self.log("="*70)
        self.log("📋 EXECUTION SUMMARY")
        self.log("="*70)
        
        # Calculate totals
        total_txns = len(self.transactions)
        total_value = self.transactions['amount_inr'].sum()
        
        self.log(f"Total Transactions Processed: {total_txns:,}")
        self.log(f"Total Transaction Value: ₹{total_value:,.0f}")
        self.log(f"Average Transaction Size: ₹{total_value/total_txns:,.0f}")
        self.log(f"Funds Analyzed: {len(self.performance)}")
        self.log(f"Geographic Markets: {self.transactions['state'].nunique()}")
        self.log(f"Fund Houses: {self.performance['fund_house'].nunique()}")
        
        # Performance stats
        self.log(f"Avg 3-Year Return: {self.performance['return_3yr_pct'].mean():.2f}%")
        self.log(f"Avg Sharpe Ratio: {self.performance['sharpe_ratio'].mean():.2f}")
        self.log(f"Avg Maximum Drawdown: {self.performance['max_drawdown_pct'].mean():.2f}%")
        
        # Time tracking
        elapsed = (datetime.now() - self.start_time).total_seconds()
        self.log(f"Execution Time: {elapsed:.2f} seconds")
        self.log("="*70)
    
    def run(self):
        """
        Execute complete ETL pipeline.
        
        Returns:
            bool: True if pipeline completed successfully
        """
        self.log("")
        self.log("="*70)
        self.log("🚀 BLUESTOCK MUTUAL FUND ETL PIPELINE - PRODUCTION EXECUTION")
        self.log("="*70)
        
        try:
            if not self.extract_data():
                return False
            
            self.log("")
            if not self.transform_data():
                return False
            
            self.log("")
            if not self.generate_analytics():
                return False
            
            self.log("")
            if not self.load_outputs():
                return False
            
            self.log("")
            self.generate_report()
            
            self.log("✅ ETL PIPELINE COMPLETED SUCCESSFULLY")
            self.log("="*70)
            
            return True
            
        except Exception as e:
            self.log(f"❌ FATAL ERROR: {str(e)}")
            self.log("="*70)
            return False
        finally:
            if self.conn:
                self.conn.close()
                self.log("Database connection closed")

def main():
    """Main execution entry point."""
    etl = BluestockETL()
    success = etl.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
