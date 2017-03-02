source /etc/esg.env
mkdir /tmp/feedback
cp test/test.json /tmp/feedback
python send_job.py $1
rm -rf /tmp/feedback*
