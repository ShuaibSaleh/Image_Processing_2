let image_input = document.querySelector('#imageFilterinput');
let imageFilter = document.querySelector('#imageFilter');
let Noise_type=document.querySelector("#Noise_type");
let Filter_Type=document.querySelector("#Filter_Type");
let SizeFilter=document.querySelector("#SizeFilter");
let submit=document.querySelector("#submit_btn");
let image_data = ""




image_input.addEventListener('change', e => {
    if (e.target.files.length) {
      const reader = new FileReader();
      reader.onload = e => {
        if (e.target.result) {
          let img = document.createElement('img');
          img.id ="imageFilter";
          img.src = e.target.result;
          imageFilter.innerHTML = '';
          imageFilter.appendChild(img)
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
      formData.append("Noise_type" ,Noise_type.value);
      formData.append("Filter_Type" ,Filter_Type.value);
      formData.append("SizeFilter" ,SizeFilter.value);
    
    
  
      $.ajax({
        type: 'POST',
        url: '/saveImg',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        async: true,
        success: function (backEndData) {
          var responce = JSON.parse(backEndData)

          let Addnoise = document.getElementById("Addnoise")
          Addnoise.remove()
          Addnoise = document.createElement("div")
          Addnoise.id = "Addnoise"
          Addnoise.innerHTML = responce[1]
          let ApplyFilter = document.getElementById("ApplyFilter")
          ApplyFilter.remove()
          ApplyFilter = document.createElement("div")
          ApplyFilter.id = "ApplyFilter"
          ApplyFilter.innerHTML = responce[2]
          let col2 = document.getElementById("Col2")
          let col3 = document.getElementById("Col3")
          col2.appendChild(Addnoise)
          col3.appendChild(ApplyFilter)


 
        }
  
  
      })
    }
     catch (error) {
      console.log("please upload two images")
    }
  
    
  }

  