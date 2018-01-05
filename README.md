# scs_psu
Communication and control of the South Coast Science power supply boards for BeagleBone.

**Required libraries:** 

* Third party: -
* SCS root: scs_core
* SCS host: scs_host_bbe, scs_host_bbe_southern, scs_host_bbe_southern


**Typical PYTHONPATH:**

BeagleBone, in /root/.bashrc:

    export PYTHONPATH=/home/debian/SCS/scs_dev/src:/home/debian/SCS/scs_osio/src:/home/debian/SCS/scs_mfr/src:/home/debian/SCS/scs_psu/src:/home/debian/SCS/scs_comms_ge910/src:/home/debian/SCS/scs_dfe_eng/src:/home/debian/SCS/scs_host_bbe/src:/home/debian/SCS/scs_core/src:$PYTHONPATH
