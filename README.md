# scs_psu
Communication and control of the South Coast Science power supply boards for BeagleBone.

**Required libraries:** 

* Third party: -
* SCS root: scs_core
* SCS host: scs_host_bbe, scs_host_bbe_southern


**Typical PYTHONPATH:**

Beaglebone, in /root/.bashrc:

export \\
PYTHONPATH=/home/debian/SCS/scs_dev:/home/debian/SCS/scs_osio:/home/debian/SCS/scs_mfr:/home/debian/SCS/scs_psu:/home/debian/SCS/scs_comms_ge910:/home/debian/SCS/scs_dfe_eng:/home/debian/SCS/scs_host_bbe:/home/debian/SCS/scs_core:$PYTHONPATH
