<script>
  export let name; 
  let contents = "";

  const socket = new WebSocket(`ws://${window.location.host}/clipboard_websocket/${name}`);

  socket.addEventListener('message', function(event) {
    contents = JSON.parse(event.data);
  });

  function tellSocket() {
    socket.send(contents);
  }
</script>

<h1>{name}</h1>
<input type="text" bind:value={contents} on:input={tellSocket}/>
<textarea readonly>{contents}</textarea>
