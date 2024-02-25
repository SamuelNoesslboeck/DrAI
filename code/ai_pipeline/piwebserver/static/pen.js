const penSubmit = document.getElementById( "penSubmit" );
const penHmin = document.getElementById( "pen-hmin" );
const penHmax = document.getElementById( "pen-hmax" );
const penSmin = document.getElementById( "pen-smin" );
const penSmax = document.getElementById( "pen-smax" );
const penVmin = document.getElementById( "pen-vmin" );
const penVmax = document.getElementById( "pen-vmax" );

const penHminValue = document.getElementById( "pen-hmin-value" );
const penHmaxValue = document.getElementById( "pen-hmax-value" );
const penSminValue = document.getElementById( "pen-smin-value" );
const penSmaxValue = document.getElementById( "pen-smax-value" );
const penVminValue = document.getElementById( "pen-vmin-value" );
const penVmaxValue = document.getElementById( "pen-vmax-value" );


const penImg = document.getElementById( "penImg" );
const penImgPixelValues = document.getElementById( "pen-image-pixel-values" );

const penCanvas = document.createElement('canvas');
const penContext = penCanvas.getContext('2d');

penImg.onload = function() {
    penCanvas.width = penImg.naturalWidth;
    penCanvas.height = penImg.naturalHeight;
    penContext.drawImage(penImg, 0, 0);
};

penImg.src = "/pen_image";

function sendpenValues(){
    hmin = penHmin.value;
    hmax = penHmax.value;

    smin = penSmin.value;
    smax = penSmax.value;

    vmin = penVmin.value;
    vmax = penVmax.value;

    fetch( "/penHSV", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax, "v-min": vmin, "v-max": vmax } )
    } )

    const penImg = document.getElementById( "penImg" );
    penImg.src = "/pen_image?" + new Date().getTime();
}


penImg.addEventListener('mousemove', function(e) {
    const rect = penImg.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);

    const pixelData = penContext.getImageData(x, y, 1, 1).data;
    penImgPixelValues.innerHTML = `${pixelData[0]}`;
});


penSubmit.onclick = function(){
    hmin = penHmin.value;
    hmax = penHmax.value;

    smin = penSmin.value;
    smax = penSmax.value;

    vmin = penVmin.value;
    vmax = penVmax.value;
    
    fetch( "/savePenValues", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax, "v-min": vmin, "v-max": vmax } )
    } )
};

penHmax.oninput = function(){ penHmaxValue.value = penHmax.value; sendpenValues(); }
penHmin.oninput = function(){ penHminValue.value = penHmin.value; sendpenValues(); }
penSmin.oninput = function(){ penSminValue.value = penSmin.value; sendpenValues(); }
penSmax.oninput = function(){ penSmaxValue.value = penSmax.value; sendpenValues(); }
penVmin.oninput = function(){ penVminValue.value = penVmin.value; sendpenValues(); }
penVmax.oninput = function(){ penVmaxValue.value = penVmax.value; sendpenValues(); }

penHmaxValue.oninput = function(){ penHmax.value = penHmaxValue.value; sendpenValues();}
penHminValue.oninput = function(){ penHmin.value = penHminValue.value; sendpenValues();}
penSminValue.oninput = function(){ penSmin.value = penSminValue.value; sendpenValues();}
penSmaxValue.oninput = function(){ penSmax.value = penSmaxValue.value; sendpenValues();}
penVminValue.oninput = function(){ penVmin.value = penVminValue.value; sendpenValues();}
penVmaxValue.oninput = function(){ penVmax.value = penVmaxValue.value; sendpenValues();}