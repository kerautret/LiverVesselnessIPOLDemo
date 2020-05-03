"""
Frangi online demo
demo editor: Bertrand Kerautret
"""

from lib import base_app, build, http, image, config
from lib.misc import app_expose, ctime
from lib.base_app import init_app

import cherrypy
from cherrypy import TimeoutError
import os.path
import shutil
import time

class app(base_app):
    """ template demo app """

    title = "Online Demonstration of  Liver Vesselness Filters  "
    xlink_article = 'http://www.ipol.im/'
    xlink_src = 'http://www.ipol.im/pub/pre/67/gjknd_1.1.tgz'
    dgtal_src = 'https://github.com/kerautret/DGtal.git'
    demo_src_filename  = 'gjknd_1.1.tgz'
    demo_src_dir = 'LiverVesselness'
    refName = "ref"
    baseName = ""
    input_nb = 1 # number of input images
    input_max_pixels = 4096 * 4096 # max size (in pixels) of an input image
    input_max_weight = 1 * 4096 * 4096 # max size (in bytes) of an input file
    input_dtype = '3x8i' # input image expected data type
    input_ext = '.png'   # input image expected extension (ie file format)
    is_test = False       # switch to False for deployment
    commands = []
    list_commands = ""
    
    def __init__(self):
        """
        app setup
        """
        # setup the parent class
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_app.__init__(self, base_dir)

        # select the base_app steps to expose
        # index() is generic
        app_expose(base_app.index)
        app_expose(base_app.input_select)
        app_expose(base_app.input_upload)
        # params() is modified from the template
        app_expose(base_app.params)
        # run() and result() must be defined here




        

    def build(self):
        """
        program build/update
        """
        # store common file path in variables
        # tgz_file = self.dl_dir + self.demo_src_filename
        # prog_names = ["dll_decomposition", "dll_sequence", "testBoundaries", \
        # 			  "testDecomposition", "testOtsu"]
        # prog_bin_files = []

        # for f in prog_names:
        #     prog_bin_files.append(self.bin_dir+ f)

        # log_file = self.base_dir + "build.log"
        # # get the latest source archive
        # print ("Starting download \n")
        # build.download(self.xlink_src, tgz_file)
        # print ("download ended... \n")
        # # test if the dest file is missing, or too old
        # if (os.path.isfile(prog_bin_files[0])
        #     and ctime(tgz_file) < ctime(prog_bin_files[0])):
        #     cherrypy.log("not rebuild needed",
        #                  context='BUILD', traceback=False)
        # else:
        #     # extract the archive
        #     build.extract(tgz_file, self.src_dir)
        #     # build the program
        #     build.run("cd %s; git clone %s" %(self.src_dir) %("https://github.com/kerautret/DGtal.git"))
        #     build.run("cd %s ; mkdir build; cmake .. -DCMAKE_BUILD_TYPE=Release; make -j 4" %(self.src_dir + "DGtal"))
            
        #     #build.run("mkdir %s;  " %(self.src_dir+"gjknd_1.1/build"), \
        #    #            						 stdout=log_file)
        #    # build.run("cd %s; cmake .. ; make -j 4" %(self.src_dir + \
        #     #							"gjknd_1.1/build"),stdout=log_file)

        #     # save into bin dir
        #     if os.path.isdir(self.bin_dir):
        #         shutil.rmtree(self.bin_dir)
        #     os.mkdir(self.bin_dir)
        #     for i in range(0, len(prog_bin_files)) :
        #         shutil.copy(self.src_dir + os.path.join("gjknd_1.1/build/src", \
        #         			prog_names[i]), prog_bin_files[i])

        #     # cleanup the source dir
        #     shutil.rmtree(self.src_dir)

        return



    def input_select_callback(self, fnames):
        '''
        Implement the callback for the input select to
        process the non-standard input
        '''         
        self.cfg['meta']['is3d'] = True
        if self.cfg['meta']['is3d'] :
            self.baseName = (fnames[0])[0:-4]
            shutil.copy(self.input_dir +self.baseName+"MaskLiver.png", self.work_dir + 'input_0MaskLiver.png')
            shutil.copy(self.input_dir +self.baseName+"MaskVessel.png", self.work_dir + 'input_0MaskVessel.png')
            #radius = (fnames[0])[-7:-4]
            radius = 50
            #self.cfg['meta']['rad'] = float(radius)
            #shutil.copy(self.input_dir +baseName+".mha",
            #            self.work_dir + 'inputVol_0.mha')        
        self.cfg.save()




    @cherrypy.expose
    @init_app
    def params(self, newrun=False, msg=None):
        """Parameter handling (optional crop)."""

        # if a new experiment on the same image, clone data
        #if newrun:
             #oldPath = self.work_dir + 'inputVol_0.mha'
             #self.clone_input()
             #shutil.copy(oldPath, self.work_dir + 'inputVol_0.mha')
             
        # save the input image as 'input_0_selection.png', the one to be used
        img = image(self.work_dir + 'input_0.png')
        img.save(self.work_dir + 'input_0_selection.png')
        img.save(self.work_dir + 'input_0_selection.pgm')


        # initialize subimage parameters
        self.cfg['param'] = {'x1':-1, 'y1':-1, 'x2':-1, 'y2':-1}
        self.cfg.save()
        return self.tmpl_out('params.html')

   



    @cherrypy.expose
    @init_app
    def wait(self, **kwargs):
        """
        params handling and run redirection
        """

        # save and validate the parameters
        
        try:
            ## Params Std 
            self.cfg['param']['sigmamin'] = kwargs['sigmamin']
            self.cfg['param']['sigmamax'] = kwargs['sigmamax']
            self.cfg['param']['steps'] = kwargs['steps']
            self.cfg['param']['masktype'] = kwargs['masktype']
            self.cfg['param']['masktypedisplay'] = kwargs['masktypedisplay']
            ## END Params Std
            
            ## Params specifics to RORPO
            self.cfg['param']['scaleminrorpo'] = kwargs['scaleminrorpo']
            self.cfg['param']['factorrorpo'] = kwargs['factorrorpo']
            self.cfg['param']['dilatationrorpo'] = kwargs['dilatationrorpo']
            self.cfg['param']['nbscalerorpo'] = kwargs['nbscalerorpo']

            ## END Params specifics to RORPO
            self.cfg['param']['sigmaoof'] = kwargs['sigmaoof']
            self.cfg['param']['methodname'] = kwargs['methodname']
            self.cfg['param']['alpha'] = kwargs['alpha']
            self.cfg['param']['beta'] = kwargs['beta']
            self.cfg['param']['gamma'] = kwargs['gamma']

            
            ## Param specific to Jerman and RuiZhang
            self.cfg['param']['tau'] = kwargs['tau']

            ## Param specific to OOF:
            self.cfg['param']['sigmaood'] = kwargs['sigmaoof']
            
            ## Param specific to Sato
            self.cfg['param']['alpha1sato'] = kwargs['alpha1sato']
            self.cfg['param']['alpha2sato'] = kwargs['alpha2sato']            

            if self.cfg['param']['methodname'] == "RORPO" :
                self.cfg['param']['methodname'] =  "RORPO_multiscale_usage"
            

            self.cfg.save()
        except ValueError:
            return self.error(errcode='badparams',
                              errmsg="The parameters must be numeric.")

        http.refresh(self.base_url + 'run?key=%s' % self.key)
        return self.tmpl_out("wait.html")

    @cherrypy.expose
    @init_app
    def run(self):
        """
        algo execution
        """

        # read the parameters
        #print self.cfg['param']

        #shutil.copy(self.input_dir +self.cfg['meta']['basename']+".vol",
        #            self.work_dir + 'inputVol_0.vol')        
        #shutil.copy(self.input_dir +self.cfg['meta']['basename']+".sdp",
        #            self.work_dir + 'inputVol_0.sdp')        
                 
        # run the algorithm
        #self.commands = ""
            
        try:
            self.run_algo(self)
        except TimeoutError:
            return self.error(errcode='timeout')
        except RuntimeError:
            return self.error(errcode='runtime',
                              errmsg="Something went wrong with the program.")
        except ValueError:
            return self.error(errcode='badparams',
                              errmsg="The parameters given produce no contours,\
                              		  please change them.")

        http.redir_303(self.base_url + 'result?key=%s' % self.key)

        # # archive
        # if self.cfg['meta']['original']:
        #     ar = self.make_archive()
        #     ar.add_file("input_0.png", "original.png", info="uploaded")
        #     ar.add_file("output.txt", info="output.txt")
        #     ar.add_file("commands.txt", info="commands.txt")
        #     ar.add_file(typeprimitive+"_out_input_0.png", info="output")
        #     ar.add_info({"type primitive": typeprimitive})
        #     ar.add_info({"use black background": b})

        #     ar.save()

        return self.tmpl_out("run.html")






    def run_algo(self, params):
        """
        the core algo runner
        could also be called by a batch processor
        this one needs no parameter
        """
        #radius = self.cfg['param']['radius']
        self.cfg['info']['run_time'] = time.time()

        ##  -------
        ## process 1: Apply Frangi
        ## ---------
        f = open(self.work_dir+"output.txt", "w")
        inputFile = self.input_dir+"Data/"+self.baseName+"/"+"patientIso.nii"
        f.write("test write output..."+ inputFile)
        fInfo = open(self.work_dir+"info.txt", "w")
        command_args = [self.cfg['param']['methodname'], '--input' , inputFile, '--output', 'res.nii']
        if self.cfg['param']['methodname'] != "RORPO_multiscale_usage" :
            command_args += ['--sigmaMin', str(float(self.cfg['param']['sigmamin'])),\
                             '--sigmaMax', str(float(self.cfg['param']['sigmamax'])),
                             '--nbSigmaSteps', str(int(self.cfg['param']['steps']))]
        else :
            command_args += ['--core','8','--scaleMin', str(float(self.cfg['param']['scaleminrorpo'])),\
                             '--nbScale', str(int(self.cfg['param']['nbscalerorpo'])),
                             '--dilationSize', str(int(self.cfg['param']['dilatationrorpo'])),
                             '--factor', str(float(self.cfg['param']['factorrorpo']))]
        ## Add specific options if a mask is selected:
        maskFile = self.input_dir+"Data/"+self.baseName+"/"+"dilatedVesselsMaskIso.nii"
        if self.cfg['param']['masktype'] == "livermask" :
            maskFile = self.input_dir+"Data/"+self.baseName+"/"+"liverMaskIso.nii"
            command_args += [ '--mask', maskFile ]
        if self.cfg['param']['masktype'] == "dilatedmask" :
            maskFile = self.input_dir+"Data/"+self.baseName+"/"+"dilatedVesselsMaskIso.nii"
            command_args += [ '--mask', maskFile ]
        if self.cfg['param']['masktype'] == "bifurcation" :
            maskFile = self.input_dir+"Data/"+self.baseName+"/"+"bifurcationsMaskIso.nii"
            command_args += [ '--mask', maskFile ]
        
        if self.cfg['param']['methodname'] == "OOF" :
            command_args += ['--sigma', str(float(self.cfg['param']['sigmaoof']))] 
        if self.cfg['param']['methodname'] == "Jerman" or  self.cfg['param']['methodname'] == "RuiZhang":
            command_args += ['--tau', str(float(self.cfg['param']['tau']))] 
        if self.cfg['param']['methodname'] == "Sato":
            command_args += ['--alpha1', str(float(self.cfg['param']['alpha1sato']))] 
            command_args += ['--alpha2', str(float(self.cfg['param']['alpha2sato']))] 
        ff = open(self.work_dir+"commands.txt", "w")
        for arg in command_args:
             self.list_commands += arg
             ff.write(arg+" ")
             
        ff.close()


        p = self.run_proc(command_args, stdout=f, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=300)
        fInfo.close()
        f.close()
        self.cfg['info']['run_time'] = time.time() - \
                                       self.cfg['info']['run_time']   

        
        # ##  -------
        # ## process 2a: Convert nii to vol
        # ## ---------
        f = open(self.work_dir+"outputMarching.txt", "w")
        fInfo= open(self.work_dir+"infoConv1.txt", "w")
        command_args = ['itk2vol', '-i' , 'res.nii', '-t', 'double','--maskImage', maskFile,\
                         '--inputMin', '0', '--inputMax','1', '-o', 'res.vol' ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
    
        # ##  -------
        # ## process 2b: Convert  vol to obj
        # ## ---------
        f = open(self.work_dir+"outputConv2.txt", "w")
        fInfo= open(self.work_dir+"infoConv2.txt", "w")
        command_args = ['volBoundary2obj', '-i' , 'res.vol', \
                         '-m','128', '-o', 'res.obj','--customDiffuse', '20', '20', '200', '200'  ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()


        # ##  -------
        # ## process 2c: convert liver mask to vol
        # ## ---------
        maskVessel = self.input_dir+"Data/"+self.baseName+"/"+"liverMaskIso.nii"
        f = open(self.work_dir+"outputVesselMask.txt", "w")
        fInfo= open(self.work_dir+"infoVesselMask.txt", "w")
        command_args = ['itk2vol', '-i' , maskVessel, '-t', 'int',\
                         '--inputMin', '0', '--inputMax','1', '-o', 'liverMask.vol' ]             
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
        
        # ##  -------
        # ## process 2c(2): convert liver mask vol to obj
        # ## ---------
        f = open(self.work_dir+"outputVesselMaskObj.txt", "w")
        fInfo= open(self.work_dir+"infoVesselMaskObj.txt", "w")
        command_args = ['volBoundary2obj', '-i' , 'liverMask.vol', \
                         '-m','128', '-o', 'vessel.obj','--customDiffuse', '200', '20', '0', '20'  ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()

        # ##  -------
        # ## process 3a: convert vessel mask to vol
        # ## ---------
        maskDilate = self.input_dir+"Data/"+self.baseName+"/"+"dilatedVesselsMaskIso.nii"
        f = open(self.work_dir+"outputDilateMask.txt", "w")
        fInfo= open(self.work_dir+"infoDilateMask.txt", "w")
        command_args = ['itk2vol', '-i' , maskDilate, '-t', 'int',\
                         '--inputMin', '0', '--inputMax','1', '-o', 'dilateMask.vol' ]             
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
        
        # ##  -------
        # ## process 3b: convert vessel mask vol to obj
        # ## ---------
        f = open(self.work_dir+"outputDilateMaskObj.txt", "w")
        fInfo= open(self.work_dir+"infoDilateMaskObj.txt", "w")
        command_args = ['volBoundary2obj', '-i' , 'dilateMask.vol', \
                         '-m','128', '-o', 'dilate.obj','--customDiffuse', '20', '200', '0', '20'  ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()


        maskFileDisplay=""
        if self.cfg['param']['masktypedisplay'] == "livermask" :
            maskFileDisplay = self.input_dir+"Data/"+self.baseName+"/"+"liverMaskIso.nii"
            if self.baseName[2:6] == "irca" :
                self.refName = "refMaskLiver"
        if self.cfg['param']['masktypedisplay'] == "dilatedmask" :
            maskFileDisplay = self.input_dir+"Data/"+self.baseName+"/"+"dilatedVesselsMaskIso.nii"
        if self.cfg['param']['masktypedisplay'] == "bifurcation" :
            maskFileDisplay = self.input_dir+"Data/"+self.baseName+"/"+"bifurcationsMaskIso.nii"

      
        # ## ----------
        # process 4 For display:
        # ## ----------
        f = open(self.work_dir+"outputMaskDisplay.txt", "w")
        fInfo= open(self.work_dir+"infoMaskDisplay.txt", "w")        
        command_args = ['itk2vol', '-i' , 'res.nii', \
                        '-o', 'res.vol','-t', 'double', '--inputMin', '0', '--inputMax',  '1' ]
        if self.cfg['param']['masktypedisplay'] != "nomask" :
           command_args += ['-m', maskFileDisplay]
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        for arg in command_args:
            self.list_commands += arg
            f.write(arg+" ")
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
        f = open(self.work_dir+"outputMaskDisplay2.txt", "w")
        fInfo= open(self.work_dir+"infoMaskDisplay2.txt", "w")
        command_args = ['vol2itk', '-i' , 'res.vol', '-o', 'res.nii' ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
 
        # ## ----------
        # process 4 For display:
        # ## ----------
        f = open(self.work_dir+"outputMaskDisplay.txt", "w")
        fInfo= open(self.work_dir+"infoMaskDisplay.txt", "w")        
        command_args = ['itk2vol', '-i' , inputFile, \
                        '-o', 'input.vol','-t', 'double', '--inputMin', '0', '--inputMax',  '1' ]
        if self.cfg['param']['masktypedisplay'] != "nomask" :
           command_args += ['-m', maskFileDisplay]
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        for arg in command_args:
            self.list_commands += arg
            f.write(arg+" ")
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
        f = open(self.work_dir+"outputMaskDisplay2.txt", "w")
        fInfo= open(self.work_dir+"infoMaskDisplay2.txt", "w")
        command_args = ['vol2itk', '-i' , 'input.vol', '-o', inputFile ]        
        p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
 
     

        # # # ##  -------
        # # # ## process 2: Apply Marching Cube
        # # # ## ---------
        # f = open(self.work_dir+"outputMarching.txt", "w")
        # fInfo = open(self.work_dir+"infoMarching.txt", "w")
        # command_args = ['3dVolMarchingCubes', '-i' , 'res.vol', '-t', str(float(self.cfg['param']['thresholdvisu'])), '-o', 'res.off' ]        
        # p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        # self.wait_proc(p, timeout=120)
        # fInfo.close()
        # f.close()
        
        # # # ##  -------
        # # # ## process 3: convert off to obj
        # # # ## ---------
        # f = open(self.work_dir+"outputConvert.txt", "w")
        # fInfo = open(self.work_dir+"infoConvert.txt", "w")
        # command_args = ['off2obj', '-i' , 'res.off', '-o', 'res2.obj', '-c', '-n' ]        
        # p = self.run_proc(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        # self.wait_proc(p, timeout=120)
        # fInfo.close()
        # f.close()
        
        


        
        return

    @cherrypy.expose
    @init_app
    def result(self, public=None):
        """
        display the algo results
        """
        return self.tmpl_out("result.html",
                             height=500, width=800)



    def runCommand(self, command, stdOut=None, stdErr=None):
        """
        Run command and update the attribute list_commands
        """
        p = self.run_proc(command, stderr=stdErr, stdout=stdOut, \
        				  env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=self.timeout)
        # transform convert.sh in it classic prog command (equivalent)
        # command_to_save = ' '.join(['"' + arg + '"' if ' ' in arg else arg
        #          for arg in command ])
        #if comp is not None:
        #    command_to_save += comp
        #self.list_commands +=  command_to_save + '\n'
        #sreturn command_to_save
