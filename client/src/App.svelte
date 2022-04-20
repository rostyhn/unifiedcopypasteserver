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

  
  function addClipboard() {
    const count = names.length + 1;
    let name = prompt("Please name the clipboard.", `Custom Clipboard ${count}`);    
    fetch(`/api/create_clipboard/${name}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'contents': 'Initial Contents', 'passphrase': ''})
    });    
  }
</script>

<main>
  <h1>Unified Copy Paste</h1>
  <p>Click / touch the name of any clipboard to automatically copy it.</p>
  {#each names as name}
    <Clipboard name={name}/>
  {/each}
  <button on:click={addClipboard}>Add clipboard</button>
</main>

<style>
  h1 {
    color: #B00020;
  }
  main {
    text-align: center;
  }
</style>
