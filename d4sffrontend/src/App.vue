<template>
  <div id="app" >
    <router-view />
  </div>
</template>
<script>
const style = 'font-weight: bold; font-size: 40px;color: red; text-shadow: 3px 3px 0 rgb(217,31,38) , 6px 6px 0 rgb(226,91,14) , 9px 9px 0 rgb(245,221,8) , 12px 12px 0 rgb(5,148,68) , 15px 15px 0 rgb(2,135,206) , 18px 18px 0 rgb(4,77,145) , 21px 21px 0 rgb(42,21,113)';
console.log('%c D4SmartFarming by Smartbits', style);

</script>
<style>

#nav {
  padding: 17px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
.bx--slider-text-input{
    display: none;
}
#colSlider > .cv-slider > .bx--slider-container{
  width: 100%;
}
#inputCursor{
  cursor: not-allowed;
}
.bx--slider__filled-track{
  background: #0f62fe!important;
}
</style>
