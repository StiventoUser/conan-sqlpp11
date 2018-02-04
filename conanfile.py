#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools

class sqlpp11Conan(ConanFile):
    name = "sqlpp11"
    version = "0.54"
    license = "BSD 2-Clause License"
    url = "https://github.com/StiventoUser/conan-sqlpp11"
    description = "A type safe embedded domain specific language for SQL queries and results in C++."
    settings = "os", "compiler", "build_type", "arch"
    requires = "date/2.4@vkrapivin/testing"
    no_copy_source = True

    def source(self):
        self.run("git clone https://github.com/rbock/sqlpp11")
        with tools.chdir("sqlpp11"):
            self.run("git checkout %s" % self.version)

    def build(self):        
        cmake = CMake(self)
        cmake.definitions["HinnantDate_ROOT_DIR"] = self.deps_cpp_info["date"].rootpath
        cmake.configure(source_dir="%s/sqlpp11" % self.source_folder)
        cmake.build()
        # Due to problem of the limitation in 260 characters in a Windows path,
        # there is a compilation error in the sqlpp11_no_conversion_operator_if_null_not_trivial test
        #cmake.test()
        cmake.install()
        
    def package_id(self):
        self.info.header_only()
