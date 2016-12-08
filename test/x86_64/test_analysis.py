import unittest
from test import equal_codes
from peachpy import *
from peachpy.x86_64 import *


class TestBasicBlockAnalysis(unittest.TestCase):
    def runTest(self):
        x = Argument(uint32_t)
        y = Argument(uint32_t)

        with Function("integer_sum", (x, y), uint32_t) as function:
            reg_x = GeneralPurposeRegister32()
            reg_y = GeneralPurposeRegister32()
            LOAD.ARGUMENT(reg_x, x)
            LOAD.ARGUMENT(reg_y, y)

            ADD(reg_x, reg_y)
            MOV(eax, reg_x)
            RETURN()

        listing = function.format_instructions()
        ref_listing = """
LOAD.ARGUMENT gp32-vreg<1>, uint32_t x
    In regs:
    Out regs:   gp64-vreg<1>
    Live regs:
    Avail regs:

LOAD.ARGUMENT gp32-vreg<2>, uint32_t y
    In regs:
    Out regs:   gp64-vreg<2>
    Live regs:  gp32-vreg<1>
    Avail regs: gp64-vreg<1>

ADD gp32-vreg<1>, gp32-vreg<2>
    In regs:    gp32-vreg<1>, gp32-vreg<2>
    Out regs:   gp64-vreg<1>
    Live regs:  gp32-vreg<1>, gp32-vreg<2>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>

MOV eax, gp32-vreg<1>
    In regs:    gp32-vreg<1>
    Out regs:   rax
    Live regs:  gp32-vreg<1>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>

RETURN
    In regs:
    Out regs:
    Live regs:
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, rax
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy listing:\n" + listing


class TestSimpleLoopAnalysis(unittest.TestCase):
    def runTest(self):
        x = Argument(ptr(const_float_))
        y = Argument(ptr(float_))
        length = Argument(size_t)

        with Function("square", (x, y, length)) as function:
            r_x = GeneralPurposeRegister64()
            r_y = GeneralPurposeRegister64()
            r_length = GeneralPurposeRegister64()
            LOAD.ARGUMENT(r_x, x)
            LOAD.ARGUMENT(r_y, y)
            LOAD.ARGUMENT(r_length, length)

            with Loop() as loop:
                xmm_value = XMMRegister()
                MOVSS(xmm_value, [r_x])
                MULSS(xmm_value, xmm_value)
                MOVSS([r_y], xmm_value)

                SUB(r_length, 1)
                JNZ(loop.begin)

            RETURN()

        listing = function.format_instructions()
        ref_listing = """
LOAD.ARGUMENT gp64-vreg<1>, const float* x
    In regs:
    Out regs:   gp64-vreg<1>
    Live regs:
    Avail regs:

LOAD.ARGUMENT gp64-vreg<2>, float* y
    In regs:
    Out regs:   gp64-vreg<2>
    Live regs:  gp64-vreg<1>
    Avail regs: gp64-vreg<1>

LOAD.ARGUMENT gp64-vreg<3>, size_t length
    In regs:
    Out regs:   gp64-vreg<3>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>

loop.begin:

MOVSS xmm-vreg<1>, [gp64-vreg<1>]
    In regs:    gp64-vreg<1>
    Out regs:   xmm-vreg<1>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>

MULSS xmm-vreg<1>, xmm-vreg<1>
    In regs:    xmm-vreg<1>
    Out regs:   xmm-vreg<1>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>

MOVSS [gp64-vreg<2>], xmm-vreg<1>
    In regs:    gp64-vreg<2>, xmm-vreg<1>
    Out regs:
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>

SUB gp64-vreg<3>, 1
    In regs:    gp64-vreg<3>
    Out regs:   gp64-vreg<3>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>

JNZ loop.begin
    In regs:
    Out regs:
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>

RETURN
    In regs:
    Out regs:
    Live regs:
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, xmm-vreg<1>
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy code:\n" + listing


class TestBFSAnalysis(unittest.TestCase):
    def runTest(self):
        vertex_edges = Argument(ptr(const_uint32_t))
        neighbors = Argument(ptr(const_uint32_t))
        input_queue = Argument(ptr(const_uint32_t))
        input_vertices = Argument(uint32_t)
        output_queue = Argument(ptr(uint32_t))
        levels = Argument(ptr(uint32_t))
        current_level = Argument(uint32_t)

        with Function("bfs",
                      (vertex_edges, neighbors, input_queue, input_vertices,
                       output_queue, levels, current_level)) as function:
            reg_vertex_edges = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_vertex_edges, vertex_edges)

            reg_neighbors = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_neighbors, neighbors)

            reg_input_queue = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_input_queue, input_queue)

            reg_input_vertices = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_input_vertices, input_vertices)

            reg_output_queue = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_output_queue, output_queue)

            reg_levels = GeneralPurposeRegister64()
            LOAD.ARGUMENT(reg_levels, levels)

            reg_current_level = GeneralPurposeRegister32()
            LOAD.ARGUMENT(reg_current_level, current_level)

            reg_output_queue_start = GeneralPurposeRegister64()
            MOV(reg_output_queue_start, reg_output_queue)

            skip_neighbor = Label("skip_neighbor")
            per_edge_loop = Loop("per_edge_loop")

            with Loop() as per_vertex_loop:
                reg_current_vertex = GeneralPurposeRegister64()
                MOV(reg_current_vertex.as_dword, [reg_input_queue])
                ADD(reg_input_queue, 4)

                reg_start_edge = GeneralPurposeRegister64()
                MOV(reg_start_edge.as_dword, [reg_vertex_edges + reg_current_vertex * 4])

                reg_end_edge = GeneralPurposeRegister64()
                MOV(reg_end_edge.as_dword, [reg_vertex_edges + reg_current_vertex * 4 + 4])

                CMP(reg_start_edge, reg_end_edge)
                JE(per_edge_loop.end)

                reg_current_neighbor_pointer = GeneralPurposeRegister64()
                LEA(reg_current_neighbor_pointer, [reg_neighbors + reg_start_edge * 4])

                reg_end_neighbor_pointer = GeneralPurposeRegister64()
                LEA(reg_end_neighbor_pointer, [reg_neighbors + reg_end_edge * 4])

                with per_edge_loop:
                    reg_neighbor_vertex = GeneralPurposeRegister64()
                    MOV(reg_neighbor_vertex.as_dword, [reg_current_neighbor_pointer])
                    ADD(reg_current_neighbor_pointer, 4)

                    reg_neighbor_level = GeneralPurposeRegister32()
                    MOV(reg_neighbor_level, [reg_levels + reg_neighbor_vertex * 4])

                    CMP(reg_neighbor_level, reg_current_level)
                    JBE(skip_neighbor)

                    MOV([reg_output_queue], reg_neighbor_vertex.as_dword)
                    ADD(reg_output_queue, 4)

                    MOV([reg_levels + reg_neighbor_vertex * 4], reg_current_level)

                    LABEL(skip_neighbor)

                    CMP(reg_current_neighbor_pointer, reg_end_neighbor_pointer)
                    JNE(per_edge_loop.begin)

                SUB(reg_input_vertices, 1)
                JNE(per_vertex_loop.begin)

            SUB(reg_output_queue, reg_output_queue_start)
            SHR(reg_output_queue, 2)
            MOV(rax, reg_output_queue)

            RETURN()

        listing = function.format_instructions()
        ref_listing = """
LOAD.ARGUMENT gp64-vreg<1>, const uint32_t* vertex_edges
    In regs:
    Out regs:   gp64-vreg<1>
    Live regs:
    Avail regs:

LOAD.ARGUMENT gp64-vreg<2>, const uint32_t* neighbors
    In regs:
    Out regs:   gp64-vreg<2>
    Live regs:  gp64-vreg<1>
    Avail regs: gp64-vreg<1>

LOAD.ARGUMENT gp64-vreg<3>, const uint32_t* input_queue
    In regs:
    Out regs:   gp64-vreg<3>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>

LOAD.ARGUMENT gp64-vreg<4>, uint32_t input_vertices
    In regs:
    Out regs:   gp64-vreg<4>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>

LOAD.ARGUMENT gp64-vreg<5>, uint32_t* output_queue
    In regs:
    Out regs:   gp64-vreg<5>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>

LOAD.ARGUMENT gp64-vreg<6>, uint32_t* levels
    In regs:
    Out regs:   gp64-vreg<6>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>

LOAD.ARGUMENT gp32-vreg<7>, uint32_t current_level
    In regs:
    Out regs:   gp64-vreg<7>
    Live regs:  gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>

MOV gp64-vreg<8>, gp64-vreg<5>
    In regs:    gp64-vreg<5>
    Out regs:   gp64-vreg<8>
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>
    Avail regs: gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>

per_vertex_loop.begin:

MOV gp32-vreg<9>, [gp64-vreg<3>]
    In regs:    gp64-vreg<3>
    Out regs:   gp64-vreg<9>
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

ADD gp64-vreg<3>, 4
    In regs:    gp64-vreg<3>
    Out regs:   gp64-vreg<3>
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>, gp64-vreg<9>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV gp32-vreg<10>, [gp64-vreg<1> + gp64-vreg<9>*4]
    In regs:    gp64-vreg<1>, gp64-vreg<9>
    Out regs:   gp64-vreg<10>
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>, gp64-vreg<9>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV gp32-vreg<11>, [gp64-vreg<1> + gp64-vreg<9>*4 + 4]
    In regs:    gp64-vreg<1>, gp64-vreg<9>
    Out regs:   gp64-vreg<11>
    Live regs:  gp32-vreg<7>, gp64-vreg<10>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>, gp64-vreg<9>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

CMP gp64-vreg<10>, gp64-vreg<11>
    In regs:    gp64-vreg<10>, gp64-vreg<11>
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

JE per_edge_loop.end
    In regs:
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

LEA gp64-vreg<12>, [gp64-vreg<2> + gp64-vreg<10>*4]
    In regs:    gp64-vreg<10>, gp64-vreg<2>
    Out regs:   gp64-vreg<12>
    Live regs:  gp32-vreg<7>, gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

LEA gp64-vreg<13>, [gp64-vreg<2> + gp64-vreg<11>*4]
    In regs:    gp64-vreg<11>, gp64-vreg<2>
    Out regs:   gp64-vreg<13>
    Live regs:  gp32-vreg<7>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

per_edge_loop.begin:

MOV gp32-vreg<14>, [gp64-vreg<12>]
    In regs:    gp64-vreg<12>
    Out regs:   gp64-vreg<14>
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

ADD gp64-vreg<12>, 4
    In regs:    gp64-vreg<12>
    Out regs:   gp64-vreg<12>
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV gp32-vreg<15>, [gp64-vreg<6> + gp64-vreg<14>*4]
    In regs:    gp64-vreg<14>, gp64-vreg<6>
    Out regs:   gp64-vreg<15>
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

CMP gp32-vreg<15>, gp32-vreg<7>
    In regs:    gp32-vreg<15>, gp32-vreg<7>
    Out regs:
    Live regs:  gp32-vreg<15>, gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

JBE skip_neighbor
    In regs:
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV [gp64-vreg<5>], gp32-vreg<14>
    In regs:    gp32-vreg<14>, gp64-vreg<5>
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

ADD gp64-vreg<5>, 4
    In regs:    gp64-vreg<5>
    Out regs:   gp64-vreg<5>
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV [gp64-vreg<6> + gp64-vreg<14>*4], gp32-vreg<7>
    In regs:    gp32-vreg<7>, gp64-vreg<14>, gp64-vreg<6>
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

skip_neighbor:

CMP gp64-vreg<12>, gp64-vreg<13>
    In regs:    gp64-vreg<12>, gp64-vreg<13>
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

JNE per_edge_loop.begin
    In regs:
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

per_edge_loop.end:

SUB gp64-vreg<4>, 1
    In regs:    gp64-vreg<4>
    Out regs:   gp64-vreg<4>
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

JNE per_vertex_loop.begin
    In regs:
    Out regs:
    Live regs:  gp32-vreg<7>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

SUB gp64-vreg<5>, gp64-vreg<8>
    In regs:    gp64-vreg<5>, gp64-vreg<8>
    Out regs:   gp64-vreg<5>
    Live regs:  gp64-vreg<5>, gp64-vreg<8>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

SHR gp64-vreg<5>, 2
    In regs:    gp64-vreg<5>
    Out regs:   gp64-vreg<5>
    Live regs:  gp64-vreg<5>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

MOV rax, gp64-vreg<5>
    In regs:    gp64-vreg<5>
    Out regs:   rax
    Live regs:  gp64-vreg<5>
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>

RETURN
    In regs:
    Out regs:
    Live regs:
    Avail regs: gp64-vreg<10>, gp64-vreg<11>, gp64-vreg<12>, gp64-vreg<13>, gp64-vreg<14>, gp64-vreg<15>, gp64-vreg<1>, gp64-vreg<2>, gp64-vreg<3>, gp64-vreg<4>, gp64-vreg<5>, gp64-vreg<6>, gp64-vreg<7>, gp64-vreg<8>, gp64-vreg<9>, rax
"""
        assert equal_codes(listing, ref_listing), "Unexpected PeachPy code:\n" + listing
