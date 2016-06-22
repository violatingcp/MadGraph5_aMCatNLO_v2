#! /usr/bin/env python
import commands,sys,os,subprocess,stat
import datetime
import time 
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
import argparse
import random

eos='/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select'
#MGrelease=

def completed(name,medrange,dmrange,basedir,carddir):
    completed = True
    for med in medrange:
        for dm in dmrange:
            if med < dm: 
                continue
            fileExists=os.path.isfile('%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s/process/run.sh' % (basedir,name,name,med,dm)) 
            if fileExists:
                #os.chmod('runcmsgrid.sh',0777)
                madgraph='%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s/mgbasedir' % (basedir,name,name,med,dm)
                process ='%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s/process'   % (basedir,name,name,med,dm)
                runcms  ='%s/runcmsgrid.sh'                           % (basedir)
                output  ='%s_%s_%s_tarball.tar.xz'                    % (name,med,dm)
                os.system('XZ_OPT="--lzma2=preset=9,dict=512MiB" tar -cJpsf '+output+' '+madgraph+' '+process+' '+runcms)
                #os.system('rm -rf %s/%s_MG5_aMC_v2_2_2/MG_%s_%s_%s' % (basedir,name,name,med,dm))
            else:
                if not os.path.isfile('MG_%s_%s_%s.tgz' % (name,med,dm)):
                    completed = False
    return completed

def replace(name,med,dm,gdm,gq,proc,rand,directory):
    gqS=gq
    gqP=gq
    gdmS=gdm
    gdmP=gdm
    gqV=gq
    gqA=gq
    gdmV=gdm
    gdmA=gdm
    gSw=gq*(80.19)*1./132.5#*(80.19)
    gPw=gq*(80.19)*1./132.5#*(80.19)
    gSb=gq*(80.19)*1./132.5/(1./(1-0.233))
    gPb=gq*(80.19)*1./132.5/(1./(1-0.233))
    if proc == 805:
        gqP=0
        gdmP=0
        gqV=0
        gqA=0
        gdmV=0
        gdmA=0
        gPw=0
        gPb=0
    elif proc == 806:
        gqS=0
        gdmS=0
        gqV=0
        gqA=0
        gdmV=0
        gdmA=0
        gSw=0
        gSb=0
    elif proc == 801:
        gqS=0
        gdmS=0
        gqP=0
        gdmP=0
        gqV=0
        gdmV=0
        gSw=0
        gSb=0
        gPw=0
        gPb=0
    else:
        gqS=0
        gdmS=0
        gqP=0
        gdmP=0
        gqA=0
        gdmA=0
        gSw=0
        gSb=0
        gPw=0
        gPb=0
    
    parameterfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]    
    for f in parameterfiles:
         with open('%s/%s_tmp' % (directory,f),"wt") as fout: 
            with open(directory+'/'+f        ,"rt") as fin: 
                for line in fin:
                    tmpline =    line.replace('X_MMED_X' ,str(med))
                    tmpline = tmpline.replace('X_MMED2_X',str(max(med,400.)))
                    tmpline = tmpline.replace('X_MDM_X' ,str(dm))
                    tmpline = tmpline.replace('X_gS_X'  ,str(gqS))
                    tmpline = tmpline.replace('X_gP_X'  ,str(gqP))
                    tmpline = tmpline.replace('X_gDMS_X',str(gdmS))
                    tmpline = tmpline.replace('X_gDMP_X',str(gdmP))
                    tmpline = tmpline.replace('X_gV_X'  ,str(gqV))
                    tmpline = tmpline.replace('X_gA_X'  ,str(gqA))
                    tmpline = tmpline.replace('X_gDMV_X',str(gdmV))
                    tmpline = tmpline.replace('X_gDMA_X',str(gdmA))
                    tmpline = tmpline.replace('X_gSw_X' ,str(gSw))
                    tmpline = tmpline.replace('X_gPw_X' ,str(gPw))
                    tmpline = tmpline.replace('X_gSb_X' ,str(gSb))
                    tmpline = tmpline.replace('X_gPb_X' ,str(gPb))
                    tmpline = tmpline.replace('X_gDMA_X',str(gdmA))
                    tmpline = tmpline.replace('MED'     ,str(med))
                    tmpline = tmpline.replace('XMASS'   ,str(dm))
                    tmpline = tmpline.replace('PROC'    ,str(proc))
                    tmpline = tmpline.replace('RAND'    ,str(rand))
                    fout.write(tmpline)
         os.system('mv %s/%s_tmp %s/%s'%(directory,f,directory,f))
 
def fileExists(filename):
   sc=None
   print '%s ls eos/cms/store/cmst3/user/pharris/gen2/%s | wc -l' %(eos,filename)
   exists = commands.getoutput('%s ls eos/cms/store/cmst3/user/pharris/gen2/%s | wc -l' %(eos,filename)  )
   if len(exists.splitlines()) > 1: 
      exists = exists.splitlines()[1]
   else:
      exists = exists.splitlines()[0]
   print exists
   return int(exists) == 1
#DMSpin1_V12j_g1
aparser = argparse.ArgumentParser(description='Process benchmarks.')
#aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/VectorMonoW/'   ,help='carddir')
#aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/VectorDiJet1Gamma/'   ,help='carddir')
#aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/DMSpin0_ggH12j/'   ,help='carddir')
#aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/DMSpin0_ggPhi12j_g1/'   ,help='carddir')
aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/DMSpin0_qqPhiz_g1/'   ,help='carddir')
#aparser.add_argument('-carddir','--carddir'   ,action='store',dest='carddir',default='Cards/DMSpin1_V12j_g1/',help='carddir')
#aparser.add_argument('-name'   ,'--name'      ,action='store',dest='name'   ,default='VectorDiJet1Gamma'       ,help='name')
aparser.add_argument('-name'   ,'--name'       ,action='store',dest='name'   ,default='DMSpin0_qqPhiz_g1'   ,help='name')
aparser.add_argument('-q'      ,'--queue'      ,action='store',dest='queue'  ,default='2nw'                   ,help='queue')
#aparser.add_argument('-dm'      ,'--dmrange'   ,dest='dmrange' ,nargs='+',type=int,default=[1,10,50,100,150,500,1000]                ,help='mass range')
#aparser.add_argument('-med'     ,'--medrange'  ,dest='medrange',nargs='+',type=int,default=[10,20,50,100,200,300,500,1000,2000,10000],help='mediator range')
aparser.add_argument('-proc'    ,'--proc'      ,dest='procrange',nargs='+',type=int,     default=[805,806],help='proc')
aparser.add_argument('-dm'      ,'--dmrange'   ,dest='dmrange' ,nargs='+',type=int,default=[1]                ,help='mass range')
aparser.add_argument('-med'     ,'--medrange'  ,dest='medrange',nargs='+',type=int,default=[125],help='mediator range')
aparser.add_argument('-gq'      ,'--gq'        ,dest='gq',nargs='+',type=int,     default=[1],help='gq')
aparser.add_argument('-gdm'     ,'--gdm'       ,dest='gdm',nargs='+',type=int,     default=[1],help='gdm')
aparser.add_argument('-resubmit','--resubmit'  ,type=bool      ,dest='resubmit',default=False,help='resubmit')
aparser.add_argument('-install' ,'--install'   ,type=bool      ,dest='install' ,default=True ,help='install MG')
aparser.add_argument('-runcms'  ,'--runcms'    ,action='store' ,dest='runcms'  ,default='runcmsgrid.sh',help='runcms')
args1 = aparser.parse_args()

print args1.carddir,args1.name,args1.queue,args1.dmrange,args1.medrange,args1.install

basedir=os.getcwd()
os.system('rm %s/%s/*~' % (basedir,args1.carddir))
##Start with the basics download Madgraph and add the options we care  :
if not args1.resubmit and args1.install:
    os.system('rm -rf /tmp/pharris/CMSSW_7_1_20')
    os.system('rm -rf /tmp/pharris/MG5_aMC_v2_3_3')
    os.system('cp  patches/install.sh .')
    os.system('./install.sh')
    os.system('mv /tmp/pharris/MG5_aMC_v2_3_3 %s_MG5_aMC_v2_3_3' % args1.name)

os.chdir ('%s_MG5_aMC_v2_3_3' %(args1.name))

##Get the base files
parameterdir   = [ f for f in listdir(basedir+'/'+args1.carddir) if not isfile(join(basedir+'/'+args1.carddir,f)) ]
parameterfiles = [ f for f in listdir(basedir+'/'+args1.carddir) if     isfile(join(basedir+'/'+args1.carddir,f)) ]
print parameterfiles,' -',basedir+'/'+args1.carddir,parameterdir

#mgcf = [f for f in parameterfiles if f.find('madconfig') > -1]
proc = [f for f in parameterfiles if f.find('proc')      > -1]
cust = [f for f in parameterfiles if f.find('custom')    > -1]
spin = [f for f in parameterfiles if f.find('madspin')   > -1]

#print "MG config :",mgcf[0]
#os.system("cp "+basedir+"/"+args1.carddir+"/%s ." % mgcf[0])
#os.system("./bin/mg5_aMC %s" % mgcf[0])

##Now build the directories iterating over options
random.seed(1)

for f in parameterdir:
    if f.find('model') == -1:
        continue
    os.system('echo cp -r %s/%s/%s models/%s' % (basedir,args1.carddir,f,f))
    os.system('cp -r %s/%s/%s models/%s' % (basedir,args1.carddir,f,f))
    os.chdir('models/%s' % (f))
    os.system('python write_param_card.py')
    os.chdir('%s/%s_MG5_aMC_v2_3_3' % (basedir,args1.name))

#Loop
for med    in args1.medrange:
    for dm in args1.dmrange:
        tmpMed = med
        if med == 2*dm:
            tmpMed = 2*dm - 5
        for pProc in args1.procrange:
            rand=random.randrange(1000,9999,1)
            if not args1.resubmit:
                for f in parameterdir:
                    #print "---->",f,'_',parameterdir
                    #if f.find('model') == -1:
                    #    continue
                    os.system('cp -r %s/%s/%s models/%s_%s_%s_%s' % (basedir,args1.carddir,f,f,tmpMed,dm,pProc))
                    os.system('echo cp -r %s/%s/%s models/%s_%s_%s' % (basedir,args1.carddir,f,f,tmpMed,dm))
                    replace(args1.name,tmpMed,dm,args1.gq[0],args1.gdm[0],pProc,rand,'models/%s_%s_%s_%s' % (f,tmpMed,dm,pProc))
                    os.chdir('models/%s_%s_%s_%s' % (f,tmpMed,dm,pProc))
                    os.system('python write_param_card.py')
                    os.chdir('%s/%s_MG5_aMC_v2_3_3' % (basedir,args1.name))
                    os.system('mkdir MG_%s_%s_%s_%s' % (args1.name,tmpMed,dm,pProc))
                
                for f in parameterfiles:
                    #print "!!!!---->",f,"--",parameterfiles
                    with open('MG_%s_%s_%s_%s/%s' % (args1.name,tmpMed,dm,pProc,f), "wt") as fout: 
                        with open(basedir+'/'+args1.carddir+'/'+f        ,"rt") as fin: 
                            for line in fin:
                                tmpline =    line.replace('MED'  ,str(tmpMed))
                                tmpline = tmpline.replace('XMASS',str(dm))
                                tmpline = tmpline.replace('PROC' ,str(pProc))
                                tmpline = tmpline.replace('RAND' ,str(random.randrange(1000,9999,1)))
                                fout.write(tmpline)
            
                job_file = open('%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/integrate.sh' % (basedir,args1.name,args1.name,tmpMed,dm,pProc), "wt")
                job_file.write('#!/bin/bash\n')
                job_file.write('cp -r %s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/  .     \n' % (basedir,args1.name,args1.name,tmpMed,dm,pProc))
                #job_file.write('cd    %s/%s_MG5_aMC_v2_2_2/MG_%s_%s_%s/        \n' % (basedir,args1.name,args1.name,med,dm))
                #job_file.write('cd - \n')
                #job_file.write('cd -  \n')
                job_file.write('scramv1 project CMSSW CMSSW_7_1_20 \n')
                job_file.write('cd CMSSW_7_1_20/src \n')
                job_file.write('eval `scramv1 runtime -sh` \n')
                job_file.write('LHAPDF6TOOLFILE=$CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/available/lhapdf6.xml \n')
                job_file.write('if [ -e $LHAPDF6TOOLFILE ]; then \n')
                job_file.write('  LHAPDFCONFIG=`cat $LHAPDF6TOOLFILE | grep "<environment name=\\"LHAPDF6_BASE\\"" | cut -d \\" -f 4`/bin/lhapdf-config \n')
                job_file.write('else \n')
                job_file.write('  LHAPDFCONFIG=`echo "$LHAPDF_DATA_PATH/../../bin/lhapdf-config"` \n')
                job_file.write('fi \n')
                job_file.write('export LHAPDF_DATA_PATH=`$LHAPDFCONFIG --datadir` \n')
                job_file.write('LHAPDFINCLUDES=`$LHAPDFCONFIG --incdir` \n')
                job_file.write('LHAPDFLIBS=`$LHAPDFCONFIG --libdir` \n')
                #job_file.write('export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/lhapdf/6.1.5/lib/ \n')
                #job_file.write('export LHAPATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/lhapdf/6.1.5/share/LHAPDF/ \n')
                job_file.write('cd - \n')
                job_file.write('cd MG_%s_%s_%s_%s/                       \n' % (args1.name,tmpMed,dm,pProc) )
                job_file.write('%s/%s_MG5_aMC_v2_3_3/bin/mg5_aMC  %s  \n' % (basedir,args1.name,proc[0]) )
                if len(cust) > 0:
                    job_file.write('cp %s %s_%s_%s_%s/                   \n' % (cust[0],args1.name,tmpMed,dm,pProc))
                    job_file.write('cd  %s_%s_%s_%s                      \n' % (args1.name,tmpMed,dm,pProc) )
                for f in parameterfiles:
                    #if f.find('dat') > -1 and f.find('run_card')  < 0:
                    #    job_file.write('mv ../%s Cards \n' % f)
                    if f.find('.f')  > -1:
                        job_file.write('mv ../%s SubProcesses \n' % f)
                job_file.write('echo "done"              >  makegrid.dat  \n')
                if len(cust) > 0:
                    job_file.write('cat %s >> makegrid.dat \n' % (cust[0]))
                job_file.write('echo "set gridpack true" >> makegrid.dat \n')
                job_file.write('echo "" >> makegrid.dat \n')
                job_file.write('echo "done">> makegrid.dat  \n')
                job_file.write('cat makegrid.dat | ./bin/generate_events pilotrun \n')
                job_file.write('cd ..      \n')
                job_file.write('mkdir process \n')
                job_file.write('mv %s_%s_%s_%s/pilotrun_gridpack.tar.gz                 process  \n' % (args1.name,tmpMed,dm,pProc))
                job_file.write('mv %s_%s_%s_%s/Events/pilotrun/unweighted_events.lhe.gz process  \n' % (args1.name,tmpMed,dm,pProc))
                job_file.write('cd process  \n')
                job_file.write('tar xzf pilotrun_gridpack.tar.gz  \n')
                job_file.write('rm pilotrun_gridpack.tar.gz  \n')
                job_file.write('echo "mg5_path = ../../mgbasedir" >> ./madevent/Cards/me5_configuration.txt \n')
                job_file.write('echo "run_mode = 0" >> ./madevent/Cards/me5_configuration.txt \n')  
                if len(spin) > 0: 
                    job_file.write('echo "import unweighted_events.lhe.gz"          >  madspinrun.dat \n')
                    job_file.write('cat %s                                          >> madspinrun.dat \n' % spin[0])
                    job_file.write('cat madspinrun.dat | MadSpin/madspin \n')
                    job_file.write('rm madspinrun.dat \n')
                    job_file.write('rm unweighted_events.lhe.gz \n')
                    job_file.write('rm -rf tmp* \n')
                    job_file.write('cp %s/%s/%s process/madspin_card.dat \n' % (basedir,args1.carddir,spin[0]))
                job_file.write('cd .. \n')
                job_file.write('cp    %s/cleangridmore.sh .      \n'  % (basedir))
                job_file.write('cp    %s/%s               runcmsgrid.sh      \n'  % (basedir,args1.runcms))
                job_file.write('./cleangridmore.sh               \n')
                job_file.write('mkdir  mgbasedir     \n')
                job_file.write('cp -r %s/%s_MG5_aMC_v2_3_3/SysCalc  mgbasedir \n' % (basedir,args1.name))
                job_file.write('cp -r %s/%s_MG5_aMC_v2_3_3/input    mgbasedir \n' % (basedir,args1.name))
                output  ='%s_%s_%s_%s_tarball.tar.xz'                    % (args1.name,tmpMed,dm,pProc)
                job_file.write('XZ_OPT="--lzma2=preset=9,dict=512MiB" tar -cJpsf '+output+' mgbasedir process runcmsgrid.sh \n')
                job_file.write('cp -r %s  %s/%s_MG5_aMC_v2_3_3/      \n' % (output,basedir,args1.name))
                job_file.close()
                os.chmod('%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/integrate.sh' % (basedir,args1.name,args1.name,tmpMed,dm,pProc),0777)
            if os.path.isfile('%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/integrate.sh' % (basedir,args1.name,args1.name,tmpMed,dm,pProc)):
                print "Looking",'%s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/integrate.sh' % (basedir,args1.name,args1.name,tmpMed,dm,pProc)
                print "Loooking More",'%s/%s_MG5_aMC_v2_3_3/%s_%s_%s_%s_tarball.tar.xz' % (basedir,args1.name,args1.name,tmpMed,dm,pProc)
                if not os.path.isfile('%s/%s_MG5_aMC_v2_3_3/%s_%s_%s_%s_tarball.tar.xz' % (basedir,args1.name,args1.name,tmpMed,dm,pProc)):
                    os.system('bsub -q  %s -R "rusage[mem=12000]" %s/%s_MG5_aMC_v2_3_3/MG_%s_%s_%s_%s/integrate.sh' % (args1.queue,basedir,args1.name,args1.name,tmpMed,dm,pProc))
            output     ='%s_%s_%s_%s_tarball.tar.xz'                    % (args1.name,tmpMed,dm,pProc)
            #lepoutput  ='%s_%s_%s_%s_lep_tarball.tar.xz'                % (args1.name,tmpMed,dm,pProc)
            #if not fileExists(lepoutput):
            #    os.system('cp ../addMadspin.sh .')
            #    os.system('bsub -q %s -o out.%%J  addMadspin.sh %s' % (args1.queue,output))
           
#while not completed(args1.name,args1.medrange,args1.dmrange,basedir,args1.carddir):
#    print "Waiting ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#    time.sleep(60)
