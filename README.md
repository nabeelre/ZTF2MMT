# ZTF2MMT
Easily add ZTF sources to the MMT/Binospec queue


## Installation
```
git clone https://github.com/nabeelre/ZTF2MMT.git
cd ZTF2MMT

conda create --name ztf2mmt python=3.11
conda activate ztf2mmt

conda env config vars set FRITZAPIKEY="KEYHERE"
conda env config vars set MMTAPIKEY="KEYHERE"
conda deactivate
conda activate ztf2mmt

pip install -r requirements.txt
pip install -e .
```

Get Fritz API key from Fritz home page -> your profile (upper right) -> scroll to bottom

Get MMT API key from MMT scheduler. The best way I know how is to look at the token variable in one of the bash download scripts.

## Usage

**NOTE** Following this example code will send a target to MMT (albeit at priority 5). Please always double-check that your targets were submitted as intended on the scheduler.

```
cd ZTF2MMT

python ztf2mmt.py --ztfid ZTF24abaixgz --exptime 900 --numexp 3 --prio 5 --notes "This is a test submission with ZTF2MMT"
```
`ztf2mmt.py` will automatically fetch the coordinates, magnitude, and finder chart from Fritz and send them to MMT.

You can also configure the following request parameters `grating`, `centwav`, `slitwidth`, `filter`. The default values are the standard transient set-up used in the Miller group: `grating=270`, `centwav=6500`, `slitwidth=Longslit1`, `filter=LP3800`.