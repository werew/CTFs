(module
  (type $type0 (func (param i32 i32) (result i32)))
  (type $type1 (func (param i32) (result i32)))
  (type $type2 (func))
  (type $type3 (func (result i32)))
  (type $type4 (func (param i32 i32 i32 i32) (result i32)))
  (import "env" "memory" (memory (;0;) 256 256))
  (import "env" "table" (table $table0 0 0 anyfunc))
  (import "env" "memoryBase" (global $global0 i32))
  (import "env" "tableBase" (global $global1 i32))
  (export "count" (func $func8))
  (export "start" (func $func5))
  (func $func0 (param $var0 i32) (param $var1 i32) (result i32)
    (local $var2 i32)
    get_local $var0
    get_local $var1
    i32.lt_s
    if
      get_local $var1
      get_local $var0
      i32.sub
      set_local $var2
    else
      get_local $var0
      get_local $var1
      i32.sub
      set_local $var2
    end
    get_local $var2
    return
  )
  (func $func1 (param $var0 i32) (result i32)
    (local $var1 i32) (local $var2 i32) (local $var3 i32) (local $var4 i32)
    block
      i32.const 0
      set_local $var2
      loop $label1
        block $label0
          get_local $var2
          i32.const 0
          i32.load8_s
          i32.const 1
          i32.sub
          i32.lt_s
          i32.eqz
          if
            br $label0
          end
          block
            get_local $var2
            i32.const 1
            i32.add
            i32.load8_s
            set_local $var3
            get_local $var2
            i32.const 1
            i32.add
            i32.const 1
            i32.add
            i32.load8_s
            set_local $var4
            get_local $var3
            get_local $var4
            call $func0
            get_local $var0
            i32.le_s
            if
              get_local $var1
              i32.const 1
              i32.add
              set_local $var1
            end
          end
          get_local $var2
          i32.const 1
          i32.add
          set_local $var2
          br $label1
        end $label0
      end $label1
    end
    get_local $var1
    return
  )
  (func $func2
    (local $var0 i32)
    loop $label1
      block $label0
        get_local $var0
        i32.const 0
        i32.load8_s
        i32.const 0
        i32.add
        i32.lt_s
        if
          get_local $var0
          i32.const 1
          i32.add
          i32.load8_s
          i32.const 9
          i32.lt_s
          if
            block
              get_local $var0
              i32.const 1
              i32.add
              get_local $var0
              i32.const 1
              i32.add
              i32.load8_s
              i32.const 1
              i32.add
              i32.store8
              br $label0
            end
          else
            block
              get_local $var0
              i32.const 1
              i32.add
              i32.const 0
              i32.store8
              get_local $var0
              i32.const 1
              i32.add
              set_local $var0
            end
          end
        else
          block
            get_local $var0
            i32.const 1
            i32.add
            i32.const 1
            i32.store8
            i32.const 0
            i32.const 0
            i32.load8_s
            i32.const 1
            i32.add
            i32.store8
            br $label0
          end
        end
        br $label1
      end $label0
    end $label1
  )
  (func $func3 (param $var0 i32) (param $var1 i32) (result i32)
    get_local $var1
    i32.eqz
    if (result i32)
      i32.const 0
    else
      get_local $var0
      get_local $var1
      i32.rem_s
    end
  )
  (func $func4 (param $var0 i32) (param $var1 i32) (result i32)
    get_local $var1
    i32.eqz
    if (result i32)
      i32.const 0
    else
      get_local $var0
      i32.const -2147483648
      i32.eq
      get_local $var1
      i32.const -1
      i32.eq
      i32.and
      if (result i32)
        i32.const 0
      else
        get_local $var0
        get_local $var1
        i32.div_s
      end
    end
  )
  (func $func5 (param $var0 i32) (result i32)
    (local $var1 i32)
    block
      i32.const 0
      set_local $var1
      loop $label1
        block $label0
          get_local $var0
          i32.const 0
          i32.gt_s
          i32.eqz
          if
            br $label0
          end
          block
            get_local $var1
            i32.const 1
            i32.add
            get_local $var0
            i32.const 10
            call $func3
            i32.store8
            get_local $var0
            i32.const 10
            call $func4
            set_local $var0
          end
          get_local $var1
          i32.const 1
          i32.add
          set_local $var1
          br $label1
        end $label0
      end $label1
    end
    i32.const 0
    get_local $var1
    i32.store8
    get_local $var1
    return
  )
  (func $func6 (result i32)
    (local $var0 i32) (local $var1 i32)
    block
      i32.const 0
      set_local $var1
      loop $label1
        block $label0
          get_local $var1
          i32.const 0
          i32.load8_s
          i32.const 0
          i32.add
          i32.lt_s
          i32.eqz
          if
            br $label0
          end
          get_local $var0
          i32.const 10
          i32.mul
          get_local $var1
          i32.const 1
          i32.add
          i32.load8_s
          i32.or
          set_local $var0
          get_local $var1
          i32.const 1
          i32.add
          set_local $var1
          br $label1
        end $label0
      end $label1
    end
    get_local $var0
    return
  )
  (func $func7 (param $var0 i32) (result i32)
    get_local $var0
    i32.load8_s
    return
  )


  (func $func8 (param $var0 i32) (param $var1 i32) (param $var2 i32) (param $var3 i32) (result i32)
    (local $var4 i32) (local $var5 i32)
    block
      get_local $var0
      set_local $var5
      loop $label1
        block $label0
          get_local $var5
          get_local $var1
          i32.const 0
          i32.add
          i32.lt_s
          i32.eqz
          if
            br $label0
          end
          block
            get_local $var2
            call $func1
            get_local $var3
            i32.le_s
            if
              get_local $var4
              i32.const 1
              i32.add
              set_local $var4
            end
            call $func2
          end
          get_local $var5
          i32.const 1
          i32.add
          set_local $var5
          br $label1
        end $label0
      end $label1
    end
    get_local $var4
    return
  )
)
