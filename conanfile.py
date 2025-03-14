# This file is managed by Conan, contents will be overwritten.
# To keep your changes, remove these comment lines, but the plugin won't be able to modify your requirements

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
import os
import subprocess

class ConanApplication(ConanFile):
    name = "werock_share"
    version = "1.0.0"
    exports_sources = "CMakeLists.txt"

    settings = "os", "compiler", "build_type", "arch"

    #def __init__(self, *args, **kwargs):
        #script_path = os.path.join(self.source_folder, "sbe/schema.xml")
        #output_path = self.build_folder
        #jar_path = os.path.join(self.source_folder, "sbe/sbe-all-1.34.1.jar")
        #output_file = os.path.join(output_path, "sbe.stub")
        #subprocess.run["java" "-Dsbe.target.language=Cpp -Dsbe.errorLog=yes -Dsbe.output.dir=%s -jar %s %s" % (output_path, jar_path, script_path), "--output", output_file]

        # output_path = os.path.join(self.build_folder, "include")
        # fbs_files = os.path.join(self.source_folder, "fbs/*.fbs")
        # output_file = os.path.join(output_path, "flatbuffers.stub")
        # subprocess.run["flatc" "--cpp -o %s %s" % (output_path, fbs_files), "--output", output_file]

    def generate(self):
        script_path = os.path.join(self.source_folder, "sbe/schema.xml")
        output_path = self.build_folder
        jar_path = os.path.join(self.source_folder, "sbe/sbe-all-1.34.1.jar")
        output_file = os.path.join(output_path, "sbe.stub")
        subprocess.run("java -Dsbe.target.language=Cpp -Dsbe.output.dir=%s -jar %s %s" % (output_path, jar_path, script_path), shell=True, check=True)

        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def requirements(self):
        self.requires("flatbuffers/24.12.23")

    def build_requirements(self):
        self.tool_requires("cmake/3.31.6")

    def build(self):

        script_path = os.path.join(self.source_folder, "sbe/schema.xml")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs  = [os.path.join(self.build_folder, "WeRock_Share_Sbe")]