#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class sqlpp11Conan(ConanFile):
    name = "sqlpp11"
    version = "0.54"
    license = "MIT"
    url = "https://github.com/StiventoUser/conan-sqlpp11"
    description = "A type safe embedded domain specific language for SQL queries and results in C++."
    settings = "os", "compiler", "build_type", "arch"
    requires = "date/2.4@vkrapivin/testing",
    no_copy_source = True
    short_paths=True

    def source(self):
        self.run("git clone https://github.com/rbock/sqlpp11")
        with tools.chdir("sqlpp11"):
            self.run("git checkout %s" % self.version)

    def build(self):        
        cmake = CMake(self)
        cmake.definitions["CMAKE_MODULE_PATH"] = ("%s;%s/cmake/Modules/" % (cmake.definitions.get("CMAKE_MODULE_PATH", ""), self.source_folder)).replace('\\', '/')
        cmake.definitions["HinnantDate_ROOT_DIR"] = self.deps_cpp_info["date"].rootpath
        # Boost (preprocessor) of version 1.50 is only required for code generation.
        #cmake.definitions["BOOST_ROOT_DIR"] = self.deps_cpp_info["boost"].rootpath
        cmake.configure(source_dir="%s/sqlpp11" % self.source_folder)
        cmake.build()
        cmake.test()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="sqlpp11/include")
        #self.copy("*.cmake", dst="cmake", src="sqlpp11/cmake")
        self.copy("*.py", dst="scripts", src="sqlpp11/scripts", keep_path=False)

    def package_id(self):
        self.info.header_only()
        #self.user_info.DLL2CPP = os.path.join(self.source_folder, "scripts", "ddl2cpp.py")
