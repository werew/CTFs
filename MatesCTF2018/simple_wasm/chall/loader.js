
function loadWasm(filename, imports = {}) {
    return fetch(filename)
      .then(response => response.arrayBuffer())
      .then(buffer => WebAssembly.compile(buffer))
      .then(module => {
        imports.env = imports.env || {}
        Object.assign(imports.env, {
          memoryBase: 0,
          tableBase: 0,
          memory: new WebAssembly.Memory({ initial: 256, maximum: 256 }),
          table: new WebAssembly.Table({ initial: 0, maximum: 0, element: 'anyfunc' })
        })
        return new WebAssembly.Instance(module, imports)
      })
  }
