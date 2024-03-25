# Farr's goal is to give programmers the sense of liberation that comes
# from the beauty of the code itself, even if it hurts productivity!
# We understand that beauty is not objective...
# https://github.com/sheikhartin/farr

from dataclasses import dataclass, field
from typing import Optional, Union, Any, List


class ASTNode:
    pass


@dataclass
class BlockNode(ASTNode):
    body: List[Union[ASTNode, Any]] = field(kw_only=True)


class ModuleNode(BlockNode):
    pass


@dataclass
class PositionedNode(ASTNode):
    row: int = field(kw_only=True)
    column: int = field(kw_only=True)


class ExpressionNode(ASTNode):
    pass


class PassNode(PositionedNode, ExpressionNode):
    pass


class NullNode(PositionedNode, ExpressionNode):
    pass


@dataclass
class HeterogeneousLiteralNode(PositionedNode, ExpressionNode):
    value: str = field(kw_only=True)


class BinaryNode(HeterogeneousLiteralNode):
    pass


class OctalNode(HeterogeneousLiteralNode):
    pass


class HexadecimalNode(HeterogeneousLiteralNode):
    pass


class IntegerNode(HeterogeneousLiteralNode):
    pass


class FloatNode(HeterogeneousLiteralNode):
    pass


class StringNode(HeterogeneousLiteralNode):
    pass


class IdentifierNode(HeterogeneousLiteralNode):
    pass


@dataclass
class RangeNode(ExpressionNode):
    from_: ExpressionNode = field(kw_only=True)
    to: Optional[ExpressionNode] = field(kw_only=True)
    by: Optional[ExpressionNode] = field(kw_only=True)


@dataclass
class ItemizedExpressionNode(ExpressionNode):
    items: List[
        Union[
            ExpressionNode,
            'VariableDeclarationNode',
            'AssignmentNode',
            Any,
        ]
    ] = field(kw_only=True)


@dataclass
class ChainedExpressionsNode(ExpressionNode):
    expressions: ItemizedExpressionNode = field(kw_only=True)


class DataStructureNode(ExpressionNode):
    pass


@dataclass
class ListNode(DataStructureNode):
    elements: ItemizedExpressionNode = field(kw_only=True)


@dataclass
class HashMapNode(DataStructureNode):
    pairs: Optional[ItemizedExpressionNode] = field(kw_only=True)


@dataclass
class PairNode(DataStructureNode):
    key: ExpressionNode = field(kw_only=True)
    value: ExpressionNode = field(kw_only=True)


@dataclass
class CallNode(ExpressionNode):
    invoke: IdentifierNode = field(kw_only=True)
    args: ItemizedExpressionNode = field(kw_only=True)


@dataclass
class GroupedExpressionNode(ExpressionNode):
    expression: ExpressionNode = field(kw_only=True)


@dataclass
class OperationNode(PositionedNode, ExpressionNode):
    operator: Optional[str] = field(kw_only=True)


@dataclass
class UnaryOperationNode(OperationNode):
    operand: ExpressionNode = field(kw_only=True)


class NegationOperationNode(UnaryOperationNode):
    pass


class PrefixOperationNode(UnaryOperationNode):
    pass


class PreIncrementNode(PrefixOperationNode):
    pass


class PreDecrementNode(PrefixOperationNode):
    pass


class PostfixOperationNode(UnaryOperationNode):
    pass


class PostIncrementNode(PostfixOperationNode):
    pass


class PostDecrementNode(PostfixOperationNode):
    pass


@dataclass
class BinaryOperationNode(OperationNode):
    left: ExpressionNode = field(kw_only=True)
    right: ExpressionNode = field(kw_only=True)


class ArithmeticOperationNode(BinaryOperationNode):
    pass


class RelationalOperationNode(BinaryOperationNode):
    pass


class LogicalOperationNode(BinaryOperationNode):
    pass


@dataclass
class TernaryOperationNode(PositionedNode, ExpressionNode):
    then: ExpressionNode = field(kw_only=True)
    condition: ExpressionNode = field(kw_only=True)
    orelse: ExpressionNode = field(kw_only=True)


class StatementNode(ASTNode):
    pass


@dataclass
class UseNode(StatementNode):
    path: ItemizedExpressionNode = field(kw_only=True)


@dataclass
class VariableDeclarationNode(StatementNode):
    identifier: IdentifierNode = field(kw_only=True)
    expression: Optional[ExpressionNode] = field(kw_only=True)


@dataclass
class AssignmentNode(StatementNode):
    references: ItemizedExpressionNode = field(kw_only=True)
    expression: ExpressionNode = field(kw_only=True)


class AggregateAssignmentNode(AssignmentNode):
    pass


class LeftShiftAssignmentNode(AggregateAssignmentNode):
    pass


class RightShiftAssignmentNode(AggregateAssignmentNode):
    pass


class AddAssignmentNode(AggregateAssignmentNode):
    pass


class SubtractAssignmentNode(AggregateAssignmentNode):
    pass


class MultiplyAssignmentNode(AggregateAssignmentNode):
    pass


class DivideAssignmentNode(AggregateAssignmentNode):
    pass


class ModulusAssignmentNode(AggregateAssignmentNode):
    pass


class PowerAssignmentNode(AggregateAssignmentNode):
    pass


@dataclass
class ControlFlowNode(StatementNode):
    condition: ExpressionNode = field(kw_only=True)
    body: BlockNode = field(kw_only=True)


@dataclass
class WhileNode(ControlFlowNode):
    orelse: Optional[BlockNode] = field(kw_only=True)


@dataclass
class ForNode(WhileNode):
    initial: ItemizedExpressionNode = field(kw_only=True)


class BreakNode(PositionedNode, StatementNode):
    pass


class ContinueNode(PositionedNode, StatementNode):
    pass


@dataclass
class IfNode(ControlFlowNode):
    orelse: Optional[
        Union[
            BlockNode,
            'IfNode',
        ]
    ] = field(kw_only=True)


@dataclass
class CaseNode(StatementNode):
    condition: ItemizedExpressionNode = field(kw_only=True)
    body: BlockNode = field(kw_only=True)
    orelse: Optional[
        Union[
            BlockNode,
            'CaseNode',
        ]
    ] = field(kw_only=True)


@dataclass
class MatchNode(StatementNode):
    expression: ExpressionNode = field(kw_only=True)
    body: BlockNode = field(kw_only=True)


@dataclass
class CatchNode(StatementNode):
    excepts: ItemizedExpressionNode = field(kw_only=True)
    as_: Optional[IdentifierNode] = field(kw_only=True)
    body: BlockNode = field(kw_only=True)
    orelse: Optional['CatchNode'] = field(kw_only=True)


@dataclass
class TryNode(StatementNode):
    body: BlockNode = field(kw_only=True)
    catch: Optional[CatchNode] = field(kw_only=True)


@dataclass
class CodeUnitNode(StatementNode):
    identifier: IdentifierNode = field(kw_only=True)
    body: Optional[Union[BlockNode, ExpressionNode]] = field(kw_only=True)


@dataclass
class FunctionDefinitionNode(CodeUnitNode):
    params: ItemizedExpressionNode = field(kw_only=True)


@dataclass
class MemberFunctionDefinitionNode(FunctionDefinitionNode):
    struct: IdentifierNode = field(kw_only=True)


@dataclass
class StructDefinitionNode(CodeUnitNode):
    parents: Optional[ItemizedExpressionNode] = field(kw_only=True)


@dataclass
class ReturnNode(PositionedNode, StatementNode):
    expression: Optional[ExpressionNode] = field(kw_only=True)
