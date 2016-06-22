#!/bin/bash

file=$1
tarfile=` echo $file     | sed "s@.xz@@g"`
barefile=`echo $file     | sed "s@.tar.xz@@g"`
dirfile=` echo $barefile | sed "s@_@ @g" | awk '{print $1"_MG5_aMC_v2_2_2"}' `
echo $file" - "$tarfile" - "$barefile" - "$dirfile
pwd
cmsStage /store/cmst3/user/pharris/gen2/$file           .
cmsStage /store/cmst3/user/pharris/gen/madspin_card.dat .
cmsStage /store/cmst3/user/pharris/gen/cleangridmore.sh .
cmsStage /store/cmst3/user/pharris/gen/${dirfile}.tgz   .
chmod +x cleangridmore.sh
unxz    $file
tar xvf $tarfile
wget --no-check-certificate https://cms-project-generators.web.cern.ch/cms-project-generators/MG5_aMC_v2.2.2.tar.gz
gunzip MG5_aMC_v2.2.2.tar.gz
tar xvf MG5_aMC_v2.2.2.tar
tar xzvf ${dirfile}.tgz
cd mgbasedir
cp -r ../MG5_aMC_v2_2_2/HELAS    .
cp -r ../MG5_aMC_v2_2_2/INSTALL  .
cp -r ../MG5_aMC_v2_2_2/LICENSE  .
cp -r ../MG5_aMC_v2_2_2/MadSpin  .
cp -r ../MG5_aMC_v2_2_2/VERSION  .
cp -r ../MG5_aMC_v2_2_2/aloha    .
cp -r ../MG5_aMC_v2_2_2/input    .
cp -r ../MG5_aMC_v2_2_2/tests    .
cp -r ../MG5_aMC_v2_2_2/vendor   .
cp -r ../MG5_aMC_v2_2_2/mg5decay .
cp -r ../MG5_aMC_v2_2_2/madgraph .
cp -r ../MG5_aMC_v2_2_2/Template .
cp -r ../${dirfile}/models       .
cd ..

cp madspin_card.dat process
scramv1 project CMSSW CMSSW_7_1_15_patch1
cd CMSSW_7_1_15_patch1/src
eval `scramv1 runtime -sh`
cd -

./runcmsgrid.sh 100 $RANDOM 1
./cleangridmore.sh
rm process/madevent/RunWeb
dir=`ls process/madevent/Events/`
echo $dir
rm -rf  process/madevent/Events/$dir

output=`echo $tarfile | sed "s@tarball@lep_tarball@g"`
echo "Creating tarball "${output}
XZ_OPT="--lzma2=preset=9,dict=512MiB" tar -cJpsf ${output}.xz mgbasedir process runcmsgrid.sh 

cmsRm    /store/cmst3/user/pharris/gen2/${tarfile}_lep.xz
cmsStage ${output}.xz /store/cmst3/user/pharris/gen2/

echo "Gridpack created successfully at ${tarfile}_lep.tar.xz"
echo "End of job"

if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 0; else exit 0; fi

