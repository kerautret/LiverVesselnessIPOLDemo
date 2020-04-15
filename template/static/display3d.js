var mesh1 = document.getElementById('mesh1').value ;    
var mesh2 = document.getElementById('mesh2').value ;    
var mesh3 = document.getElementById('mesh3').value ;    

var liverVisible=true;
var dilateVisible=true;
var vesselVisible=true;
var beginDilate = 0;
var endDilate = 0; 
var beginVessel = 0;
var endVessel = 0; 
var beginLiver = 0;
var endLiver = 0; 
var canvas;
var viewer;
var theScene = new JSC3D.Scene;

var theNewScene = new JSC3D.Scene;

var numOfLoaded = 0;
var loadVessel = false;
var loadLiver = false;
var loadDilate = false;
var loadRef = false;
var com = function (){ console.debug("complete!!!");};

function init() {
    canvas = document.getElementById('cv');
    viewer = new JSC3D.Viewer(canvas);
    
    viewer.setParameter('SceneUrl', mesh1 );
    viewer.setParameter('InitRotationX', -20);
    viewer.setParameter('InitRotationY', 20);
    viewer.setParameter('InitRotationZ', 0);
    viewer.setParameter('ModelColor', '#808080');
    viewer.setParameter('BackgroundColor1', '#FFFFFF');
    viewer.setParameter('BackgroundColor2', '#EEEEFF');
    viewer.setParameter('RenderMode', 'flat');
    viewer.setParameter('Renderer', 'webgl');
    viewer.setParameter('FaceCulling', 'on');
    viewer.init();
    viewer.update();
    viewer.onloadingcomplete = function (){
        if (!loadVessel)
        {
            loadModelVessel();
            loadModelLiver();
        }
    };
}

var addModel = function(scene) {
    var meshes = scene.getChildren();
    var s = viewer.getScene();
    for (var i=0; i<meshes.length; i++) {
        s.addChild(meshes[i]);
        console.debug("add mesh:",i);
    }
    viewer.replaceScene(s);

    
};



function updateVisible()
{
    var meshes = viewer.getScene().getChildren();
            meshes[2].visible=liverVisible;

            meshes[1].visible=vesselVisible;

            meshes[0].visible=dilateVisible;

    viewer.update();
}

function loadModelVessel() {
    beginDilate=0;
    endDilate=viewer.getScene().getChildren().length-1;
        loadVessel=true;
        var model = mesh3;
        var loader = new JSC3D.ObjLoader;
        loader.onload = addModel;
        loader.loadFromUrl(model);

}

function loadModelLiver() {
    beginVessel=endDilate+1;
    endVessel=viewer.getScene().getChildren().length-1;
    beginLiver=viewer.getScene().getChildren().length;
        loadLiver=true;
        var model = mesh2;
        var loader = new JSC3D.ObjLoader;
        loader.onload = addModel;
        loader.loadFromUrl(model);
    
}



function switchLiver(){
    liverVisible=!liverVisible;
    updateVisible();
}
function switchDilate(){
    dilateVisible=!dilateVisible;
    updateVisible();
}
function switchVessel(){
    vesselVisible=!vesselVisible;
    updateVisible();
}
