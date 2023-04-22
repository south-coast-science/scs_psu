# scs_psu
Communication and control of the South Coast Science power supply boards

_Contains library classes only._


**Required libraries:** 

* Third party: -
* SCS root: scs_core
* SCS host: scs_host_bbe, scs_host_bbe_southern, scs_host_bbe_southern


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_psu.git


**Example PYTHONPATH:**

BeagleBone, in /root/.bashrc:

    export PYTHONPATH=/home/debian/SCS/scs_dev/src:/home/debian/SCS/scs_mfr/src:/home/debian/SCS/scs_psu/src:/home/debian/SCS/scs_comms_ge910/src:/home/debian/SCS/scs_dfe_eng/src:/home/debian/SCS/scs_host_bbe/src:/home/debian/SCS/scs_core/src:$PYTHONPATH
