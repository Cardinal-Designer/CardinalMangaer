add_rules("plugin.compile_commands.autoupdate", {outputdir = ".vscode"})
add_rules("mode.debug", "mode.release")

add_requires("libadwaita-1",{system = true})

target("CardinalManager")
  set_kind("binary")
  add_ldflags("-mwindows")

  add_files("CardinalManager/src/**.c")
  add_includedirs("CardinalManager/src")
  add_packages("libadwaita-1")


  after_install(function (target)
    if is_plat("windows") then
      os.exec("python \"$(projectdir)/Script/autocopy.py\" $(projectdir)/%s $(projectdir)/%s/bin",
              target:targetfile(),target:installdir())
    end
  end)

