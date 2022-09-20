# Generated by Django 3.2.6 on 2021-11-01 09:38
import django.db.models.deletion
from django.db import migrations, models

from baserow.contrib.database.formula import (
    BaserowFormula,
    BaserowFormulaVisitor,
    FormulaHandler,
)

# noinspection PyPep8Naming


def reverse(apps, schema_editor):
    pass


# noinspection PyPep8Naming
def forward(apps, schema_editor):
    Field = apps.get_model("database", "Field")
    FormulaField = apps.get_model("database", "FormulaField")
    FieldDependency = apps.get_model("database", "FieldDependency")
    LinkRowField = apps.get_model("database", "LinkRowField")

    _build_graph_from_scratch(FieldDependency, FormulaField, LinkRowField, Field)


def convert_string_literal_token_to_string(string_literal, is_single_q):
    literal_without_outer_quotes = string_literal[1:-1]
    quote = "'" if is_single_q else '"'
    return literal_without_outer_quotes.replace("\\" + quote, quote)


class BaserowFieldReferenceVisitor(BaserowFormulaVisitor):
    def visitRoot(self, ctx: BaserowFormula.RootContext):
        return ctx.expr().accept(self)

    def visitStringLiteral(self, ctx: BaserowFormula.StringLiteralContext):
        return set()

    def visitDecimalLiteral(self, ctx: BaserowFormula.DecimalLiteralContext):
        return set()

    def visitBooleanLiteral(self, ctx: BaserowFormula.BooleanLiteralContext):
        return set()

    def visitBrackets(self, ctx: BaserowFormula.BracketsContext):
        return ctx.expr().accept(self)

    def visitFunctionCall(self, ctx: BaserowFormula.FunctionCallContext):
        args = set()
        for expr in ctx.expr():
            args.update(expr.accept(self))
        return args

    def visitFunc_name(self, ctx: BaserowFormula.Func_nameContext):
        return set()

    def visitIdentifier(self, ctx: BaserowFormula.IdentifierContext):
        return set()

    def visitIntegerLiteral(self, ctx: BaserowFormula.IntegerLiteralContext):
        return set()

    def visitFieldReference(self, ctx: BaserowFormula.FieldReferenceContext):
        reference = ctx.field_reference()
        field_name = convert_string_literal_token_to_string(
            reference.getText(), reference.SINGLEQ_STRING_LITERAL()
        )
        return {field_name}

    def visitFieldByIdReference(self, ctx: BaserowFormula.FieldByIdReferenceContext):
        return set()

    def visitLeftWhitespaceOrComments(
        self, ctx: BaserowFormula.LeftWhitespaceOrCommentsContext
    ):
        return ctx.expr().accept(self)

    def visitRightWhitespaceOrComments(
        self, ctx: BaserowFormula.RightWhitespaceOrCommentsContext
    ):
        return ctx.expr().accept(self)


# noinspection PyPep8Naming
def _build_graph_from_scratch(FieldDependency, FormulaField, LinkRowField, Field):
    for link_row in LinkRowField.objects.filter(trashed=False).all():
        related_primary_field = link_row.link_row_table.field_set.filter(
            trashed=False
        ).get(primary=True)
        FieldDependency.objects.create(
            dependant=link_row, via=link_row, dependency=related_primary_field
        )

    for formula in FormulaField.objects.filter(trashed=False).all():
        tree = FormulaHandler.get_parse_tree_for_formula(formula.formula)
        dependency_field_names = tree.accept(BaserowFieldReferenceVisitor()) or set()
        table = formula.table
        for new_dependency_field_name in dependency_field_names:
            try:
                FieldDependency.objects.create(
                    dependency=table.field_set.filter(trashed=False).get(
                        name=new_dependency_field_name
                    ),
                    dependant=formula,
                )
            except Field.DoesNotExist:
                FieldDependency.objects.create(
                    dependant=formula,
                    broken_reference_field_name=new_dependency_field_name,
                )


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0043_webhooks"),
    ]

    operations = [
        migrations.CreateModel(
            name="FieldDependency",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "broken_reference_field_name",
                    models.TextField(blank=True, null=True, db_index=True),
                ),
                (
                    "dependant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependencies",
                        to="database.field",
                    ),
                ),
                (
                    "dependency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependants",
                        to="database.field",
                    ),
                ),
                (
                    "via",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vias",
                        to="database.linkrowfield",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="formulafield",
            name="version",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="field",
            name="field_dependencies",
            field=models.ManyToManyField(
                related_name="dependant_fields",
                through="database.FieldDependency",
                to="database.Field",
            ),
        ),
        migrations.AddField(
            model_name="formulafield",
            name="internal_formula",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="formulafield",
            name="requires_refresh_after_insert",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.RunPython(forward, reverse),
    ]