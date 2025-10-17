function GenerateBarGraph(value){
    let data=JSON.parse(value);
    let ProductName=data.map((item)=>{return item[0]});
    let Quantity=data.map((item)=>{return item[1]});
    let canvas=document.getElementById('mychart');
    const config = {
  type: 'bar',
  data: {
    labels:ProductName,
    datasets:[{
      label:"Display's Total No of Product",
      data:Quantity,
      borderWidth:1,
          backgroundColor: [
        'rgba(255, 99, 132, 0.6)',   // red
        'rgba(54, 162, 235, 0.6)',   // blue
        'rgba(255, 206, 86, 0.6)',   // yellow
        'rgba(75, 192, 192, 0.6)'    // green
    ],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)'
    ],
    }]
  },
  options: {
    scales:{
        y:{
            beginatZero:true,
        }
    }
    }
  };
     new Chart(canvas,config);
}