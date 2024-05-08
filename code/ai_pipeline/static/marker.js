const markerSubmit = document.getElementById( "markerSubmit" );
const markerHmin = document.getElementById( "marker-hmin" );
const markerHmax = document.getElementById( "marker-hmax" );
const markerSmin = document.getElementById( "marker-smin" );
const markerSmax = document.getElementById( "marker-smax" );

const markerHminValue = document.getElementById( "marker-hmin-value" );
const markerHmaxValue = document.getElementById( "marker-hmax-value" );
const markerSminValue = document.getElementById( "marker-smin-value" );
const markerSmaxValue = document.getElementById( "marker-smax-value" );

const markerImg = document.getElementById( "markerImg" );
const markerImgPixelValues = document.getElementById( "marker-image-pixel-values" );

const markerCanvas = document.createElement('canvas');
const markerContext = markerCanvas.getContext('2d');

markerImg.onload = function() {
    markerCanvas.width = markerImg.naturalWidth;
    markerCanvas.height = markerImg.naturalHeight;
    markerContext.drawImage(markerImg, 0, 0);
};

markerImg.src = "/marker_image";

function sendMarkerValues(){
    hmin = markerHmin.value;
    hmax = markerHmax.value;
    smin = markerSmin.value;
    smax = markerSmax.value;

    fetch( "/markerHSV", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax } )
    } )

    const markerImg = document.getElementById( "markerImg" );
    markerImg.src = "/marker_image?" + new Date().getTime();

    sendpaperValues();
}


markerImg.addEventListener('mousemove', function(e) {
    const rect = markerImg.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);
    // Get pixel data
    const pixelData = markerContext.getImageData(x, y, 1, 1).data;
    markerImgPixelValues.innerHTML = `${pixelData[0]}`;
});


markerSubmit.onclick = function(){
    hmin = markerHmin.value;
    hmax = markerHmax.value;
    smin = markerSmin.value;
    smax = markerSmax.value;
    
    fetch( "/saveMarkerValues", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax } )
    } )
};
markerHmax.oninput = function(){ markerHmaxValue.value = markerHmax.value; sendMarkerValues(); }
markerHmin.oninput = function(){ markerHminValue.value = markerHmin.value; sendMarkerValues(); }
markerSmin.oninput = function(){ markerSminValue.value = markerSmin.value; sendMarkerValues(); }
markerSmax.oninput = function(){ markerSmaxValue.value = markerSmax.value; sendMarkerValues(); }

markerHmaxValue.oninput = function(){ markerHmax.value = markerHmaxValue.value; sendMarkerValues();}
markerHminValue.oninput = function(){ markerHmin.value = markerHminValue.value; sendMarkerValues();}
markerSminValue.oninput = function(){ markerSmin.value = markerSminValue.value; sendMarkerValues();}
markerSmaxValue.oninput = function(){ markerSmax.value = markerSmaxValue.value; sendMarkerValues();}