import Lake
open Lake DSL

package «proofs» {
  -- add package configuration options here
}

lean_lib «Proofs» {
  -- add library configuration options here
}

@[default_target]
lean_exe «certify» {
  root := `Main
}

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"
