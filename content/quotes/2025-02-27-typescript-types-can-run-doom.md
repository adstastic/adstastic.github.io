---
title: "TypeScript Types Can Run DOOM"
date: 2025-02-27
ref: https://simonwillison.net/2025/Feb/27/typescript-types-can-run-doom/#atom-everything
---


Quoting [Simon Willison](https://simonwillison.net/2025/Feb/27/typescript-types-can-run-doom/#atom-everything):

> The end result was 177TB of data representing 3.5 trillion lines of type definitions. Rendering the first frame of DOOM took 12 days running at 20 million type instantiations per second.

Here's [the source code](https://github.com/MichiganTypeScript/typescript-types-only-wasm-runtime) for the WASM runtime. The code for [Add](https://github.com/MichiganTypeScript/typescript-types-only-wasm-runtime/blob/master/packages/ts-type-math/add.ts) and [Divide](https://github.com/MichiganTypeScript/typescript-types-only-wasm-runtime/blob/master/packages/ts-type-math/divide.ts) provides a neat example of