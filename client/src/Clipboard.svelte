<script>
  export let name;   
  let contents = "";

  const socket = new WebSocket(`ws://${window.location.host}/api/clipboard_websocket/${name}`);

  socket.addEventListener('message', function(event) {
    contents = JSON.parse(event.data);
  });

  function tellSocket() {
    socket.send(contents);
  }

 function copyToClipboard() {
   let el = document.getElementById(name);  
      
   var oldContentEditable = el.contentEditable,
       oldReadOnly = el.readOnly,
       range = document.createRange();
   
   el.contentEditable = true;
   el.readOnly = false;
   range.selectNodeContents(el);

   var s = window.getSelection();
   s.removeAllRanges();
   s.addRange(range);
      
   el.setSelectionRange(0, el.value.length); 
      
   el.contentEditable = oldContentEditable;
   el.readOnly = oldReadOnly;
      
   document.execCommand('copy');
 }

</script>

<div>
  <h2 on:click={copyToClipboard}>{name}</h2>
  <textarea bind:value={contents} on:input={tellSocket} id={name}/>
</div>

<style>
  h2 {
    
  }
  textarea {
    width: 40%;
    resize: none;
  }
</style>
