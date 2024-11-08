#!/bin/bash

cd /home/big/AstroChimps
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:`pwd`

# Sleep is used to ensure database_creator connects to internet before calling a get command
sleep 30

python /home/big/AstroChimps/programs/database_creation/database_creator_generic_01.py >> /home/big/AstroChimps/logs/maintenance_logs/output_dcg.txt &
python /home/big/AstroChimps/bin/program_main.py >> /home/big/AstroChimps/logs/maintenance_logs/output_program_main.txt &
