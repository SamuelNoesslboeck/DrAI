const paperSubmit = document.getElementById( "paperSubmit" );
const paperHmin = document.getElementById( "paper-hmin" );
const paperHmax = document.getElementById( "paper-hmax" );
const paperSmin = document.getElementById( "paper-smin" );
const paperSmax = document.getElementById( "paper-smax" );

const paperHminValue = document.getElementById( "paper-hmin-value" );
const paperHmaxValue = document.getElementById( "paper-hmax-value" );
const paperSminValue = document.getElementById( "paper-smin-value" );
const paperSmaxValue = document.getElementById( "paper-smax-value" );


const paperImg = document.getElementById( "paperImg" );
const paperImgPixelValues = document.getElementById( "paper-image-pixel-values" );

const paperCanvas = document.createElement('canvas');
const paperContext = paperCanvas.getContext('2d');

paperImg.onload = function() {
    paperCanvas.width = paperImg.naturalWidth;
    paperCanvas.height = paperImg.naturalHeight;
    paperContext.drawImage(paperImg, 0, 0);
};

paperImg.src = "/paper_image";

function sendpaperValues(){
    hmin = paperHmin.value;
    hmax = paperHmax.value;
    smin = paperSmin.value;
    smax = paperSmax.value;

    fetch( "/paperHSV", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax } )
    } )

    const paperImg = document.getElementById( "paperImg" );
    paperImg.src = "/paper_image?" + new Date().getTime();

    sendpenValues()
}


paperImg.addEventListener('mousemove', function(e) {
    const rect = paperImg.getBoundingClientRect();
    const x = (e.clientX - rect.left);
    const y = (e.clientY - rect.top);

    const pixelData = paperContext.getImageData(x, y, 1, 1).data;
    paperImgPixelValues.innerHTML = `${pixelData[0]}`;
});


paperSubmit.onclick = function(){
    hmin = paperHmin.value;
    hmax = paperHmax.value;
    smin = paperSmin.value;
    smax = paperSmax.value;
    
    fetch( "/savePaperValues", { 
        method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        method: "POST",

        body: JSON.stringify( { "h-min": hmin, "h-max": hmax, "s-min": smin, "s-max": smax } )
    } )
};
paperHmax.oninput = function(){ paperHmaxValue.value = paperHmax.value; sendpaperValues(); }
paperHmin.oninput = function(){ paperHminValue.value = paperHmin.value; sendpaperValues(); }
paperSmin.oninput = function(){ paperSminValue.value = paperSmin.value; sendpaperValues(); }
paperSmax.oninput = function(){ paperSmaxValue.value = paperSmax.value; sendpaperValues(); }

paperHmaxValue.oninput = function(){ paperHmax.value = paperHmaxValue.value; sendpaperValues();}
paperHminValue.oninput = function(){ paperHmin.value = paperHminValue.value; sendpaperValues();}
paperSminValue.oninput = function(){ paperSmin.value = paperSminValue.value; sendpaperValues();}
paperSmaxValue.oninput = function(){ paperSmax.value = paperSmaxValue.value; sendpaperValues();}