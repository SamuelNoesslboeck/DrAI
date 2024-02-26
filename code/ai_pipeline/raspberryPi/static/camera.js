
const brightness = document.getElementById( "brightness" );
const sharpness = document.getElementById( "sharpness" );
const contrast = document.getElementById( "contrast" );

const brightnessValue = document.getElementById( "brightness-value" );
const sharpnessValue = document.getElementById( "sharpness-value" );
const contrastValue = document.getElementById( "contrast-value" );

brightness.oninput = function(){ brightnessValue.value = brightness.value; capture(); }
sharpness.oninput = function(){ sharpnessValue.value = sharpness.value; capture(); }
contrast.oninput = function(){ contrastValue.value = contrast.value; capture(); }

brightnessValue.oninput = function(){ brightness.value = brightnessValue.value; capture(); }
sharpnessValue.oninput = function(){ sharpness.value = sharpnessValue.value; capture(); }
contrastValue.oninput = function(){ contrast.value = contrastValue.value; capture(); }


function capture(){
    brightnessV = brightness.value;
    sharpnessV = sharpness.value;
    contrastV = contrast.value; 

    fetch( "/take_image",
    {   method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify( { "brightness": brightnessV, "sharpness": sharpnessV, "contrast": contrastV } )
    } )

    setTimeout( () => {
        const originalImg = document.getElementById( "originalImg" );
        originalImg.src = "/original?" + new Date().getTime();
        sendMarkerValues();
    }, 5000 )
}

function saveValues(){
    brightnessV = brightness.value;
    sharpnessV = sharpness.value;
    contrastV = contrast.value; 

    fetch( "/saveCameraValues",
    {   method : "POST",
        mode: 'no-cors',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify( { "brightness": brightnessV, "sharpness": sharpnessV, "contrast": contrastV } )
    } )
}

const cameraSubmit = document.getElementById( "cameraSubmit" );
cameraSubmit.onclick = saveValues;
