<svelte:head>
<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu" />
</svelte:head>
<script>
  import Clipboard from './Clipboard.svelte';
  
  const socket = new WebSocket(`ws://${window.location.host}/clipboards_websocket`);
  let names = [];
  socket.addEventListener('message', function(event) {
    names = JSON.parse(event.data);
  });
</script>

<main>
  <h1>Unified Copy Paste</h1>
  {#each names as name}
    <Clipboard name={name}/>
    {/each} 
</main>

<style>
  main {
    text-align: center;
  }
</style>
