let image_input = document.querySelector('#imageinput');
let imagetoshow = document.querySelector('#inputImage');
let imageoutput=document.querySelector("#imageoutput");
let imageNormalization=document.querySelector("#imageNormalization");
let histimageNormalization=document.querySelector("#histimageNormalization");
let selectEqual=document.querySelector("#selectEqual")
let submit=document.querySelector("#submit_btn");
let image_data = ""




image_input.addEventListener('change', e => {
    if (e.target.files.length) {
      const reader = new FileReader();
      reader.onload = e => {
        if (e.target.result) {
          let img = document.createElement('img');
          img.id ="inputImage";
          img.src = e.target.result;
          imagetoshow.innerHTML = '';
          imagetoshow.appendChild(img)
          image_data = e.target.result
         
          
        }
      };
      reader.readAsDataURL(e.target.files[0]);
     
    }
    
  });

submit.addEventListener('click', e => {
e.preventDefault();
send();
}
)


    
function send(){
  
      let formData = new FormData();

      try {

       if (image_data == "") {
        throw "error : not enought images "
      }
      formData.append('path',image_data);
      formData.append("option" ,selectEqual.value)
 
    
  
  
      $.ajax({
        type: 'POST',
        url: '/normalizationserver',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        async: true,
        success: function (backEndData) {

          var responce = JSON.parse(backEndData)
          let imageoutput = document.getElementById("imageoutput");
          imageoutput.remove();
          imageoutput = document.createElement("div");
          imageoutput.id = "imageoutput";
          imageoutput.innerHTML = responce[1];


        
          let imageNormalization = document.getElementById("imageNormalization");
          imageNormalization.remove();
          imageNormalization = document.createElement("div");
          imageNormalization.id = "imageNormalization";
          imageNormalization.innerHTML = responce[2];

          let histimageNormalization = document.getElementById("histimageNormalization");
          histimageNormalization.remove();
          histimageNormalization = document.createElement("div");
          histimageNormalization.id = "histimageNormalization";
          histimageNormalization.innerHTML = responce[3];


          let col2 = document.getElementById("Col2");
          let col3 = document.getElementById("Col3");
          let Col4 =document.getElementById("Col4")
          col2.appendChild(imageoutput);
          col3.appendChild(imageNormalization);
          Col4.appendChild(histimageNormalization)


 
  


 
        }
  
  
      })
    }
     catch (error) {
      console.log("please upload two images")
    }
  
    
  }

  