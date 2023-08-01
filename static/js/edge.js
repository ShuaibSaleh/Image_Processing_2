let image_input = document.querySelector('#imageinput');
let imageEdges = document.querySelector('#imageEdges');
let edgedetect_method=document.querySelector("#edgedetectmethod");
let submit=document.querySelector("#submit_btn");
let image_data = ""




image_input.addEventListener('change', e => {
    if (e.target.files.length) {
      const reader = new FileReader();
      reader.onload = e => {
        if (e.target.result) {
          let img = document.createElement('img');
          img.id ="imageEdges";
          img.src = e.target.result;
          imageEdges.innerHTML = '';
          imageEdges.appendChild(img)
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
      formData.append("edgedetectmethod" ,edgedetect_method.value);

    
      console.log("formdata done")
      $.ajax({
        type: 'POST',
        url: '/edgeImg',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        async: true,
        success: function (backEndData) {
          var responce = JSON.parse(backEndData)

          let ApplyEdges = document.getElementById("ApplyEdges")
          ApplyEdges.remove()
          ApplyEdges = document.createElement("div")
          ApplyEdges.id = "ApplyEdges"
          ApplyEdges.innerHTML = responce[1]
          
          let col2 = document.getElementById("Col2")
          col2.appendChild(ApplyEdges)
        }
      })
      console.log("ajax done")
    }
     catch (error) {
      console.log("please upload two images")
    } 
  }