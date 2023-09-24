add_rules("plugin.compile_commands.autoupdate", {outputdir = ".vscode"})
add_rules("mode.debug", "mode.release")

add_requires("libadwaita-1",{system = true})

target("CardinalManager")
  set_kind("binary")
  add_files("src/**.c")
  add_includedirs("src")
  add_packages("libadwaita-1")

  after_build(function (target)
    if is_plat("windows") then
      local outdata, errdata = os.iorun("python \"$(projectdir)/Script/autocopy.py\" $(projectdir)/%s $(projectdir)/%s",target:targetfile(),target:targetdir())
      print(outdata)
    end
  end)

