const personalStylist = document.getElementById('personal')
const generalStylist = document.getElementById('general')
const recBox = document.getElementById('recommendation')

console.log('hey') 
const tips = ['Not sure where to start when building a new wardrobe? Always start with basics that can be paired with many things. You will have a lot more variation in your wardrobe!', 'Accessories, accessories, accessories! Adding accessories to even the most basic outfits will elevate your look and allow your personality to shine through', 'When in doubt, turn to color theory! Looking at a color wheel will help you choose colors that pair well with one another when you lack inspiration!']


const personalTips = () => {
  
  
}

const generalTips = () => {
  
  let tipselect = Math.floor(Math.random()*(tips.length)) 

  let newTip = document.createElement('p')
  newTip.innerHTML = tips[tipselect]

  
  recBox.appendChild(newTip)
  console.log('clicked')
    
  setTimeout(() => {
    recBox.removeChild(newTip)}, 5000)


}

generalStylist.addEventListener('click', generalTips)