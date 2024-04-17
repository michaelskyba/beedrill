<script>
	export let pageLinked;
	export let text;

	const click = () => {
		alert(pageLinked)
	}
</script>

<button on:click={click}>{text}</button>
