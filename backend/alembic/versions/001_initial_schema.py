"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-10-16

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema"""
    
    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('unit_system', sa.String(), default='SI_mm'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_id', 'projects', ['id'])
    
    # Nodes table
    op.create_table(
        'nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('node_id', sa.String(), nullable=False),
        sa.Column('x', sa.Float(), nullable=False),
        sa.Column('y', sa.Float(), nullable=False),
        sa.Column('z', sa.Float(), nullable=False),
        sa.Column('restraints', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'node_id', name='uq_project_node')
    )
    op.create_index('ix_nodes_id', 'nodes', ['id'])
    op.create_index('ix_nodes_project_id', 'nodes', ['project_id'])
    
    # Elements table
    op.create_table(
        'elements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('element_id', sa.String(), nullable=False),
        sa.Column('node_i', sa.String(), nullable=False),
        sa.Column('node_j', sa.String(), nullable=False),
        sa.Column('element_type', sa.String(), nullable=False),
        sa.Column('material_id', sa.String(), nullable=True),
        sa.Column('section_type', sa.String(), nullable=True),
        sa.Column('width', sa.Float(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'element_id', name='uq_project_element')
    )
    op.create_index('ix_elements_id', 'elements', ['id'])
    op.create_index('ix_elements_project_id', 'elements', ['project_id'])
    
    # Materials table
    op.create_table(
        'materials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('material_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('E', sa.Float(), nullable=False),
        sa.Column('nu', sa.Float(), nullable=False),
        sa.Column('density', sa.Float(), nullable=False),
        sa.Column('fy', sa.Float(), nullable=True),
        sa.Column('fu', sa.Float(), nullable=True),
        sa.Column('material_type', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'material_id', name='uq_project_material')
    )
    op.create_index('ix_materials_id', 'materials', ['id'])
    op.create_index('ix_materials_project_id', 'materials', ['project_id'])
    
    # Sections table
    op.create_table(
        'sections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('section_type', sa.String(), nullable=False),
        sa.Column('A', sa.Float(), nullable=False),
        sa.Column('Iy', sa.Float(), nullable=False),
        sa.Column('Iz', sa.Float(), nullable=False),
        sa.Column('J', sa.Float(), nullable=False),
        sa.Column('depth', sa.Float(), nullable=True),
        sa.Column('width', sa.Float(), nullable=True),
        sa.Column('flange_thickness', sa.Float(), nullable=True),
        sa.Column('web_thickness', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'section_id', name='uq_project_section')
    )
    op.create_index('ix_sections_id', 'sections', ['id'])
    op.create_index('ix_sections_project_id', 'sections', ['project_id'])
    
    # Loads table
    op.create_table(
        'loads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('load_id', sa.String(), nullable=False),
        sa.Column('load_type', sa.String(), nullable=False),
        sa.Column('load_case', sa.String(), nullable=False),
        sa.Column('target_id', sa.String(), nullable=False),
        sa.Column('fx', sa.Float(), nullable=True),
        sa.Column('fy', sa.Float(), nullable=True),
        sa.Column('fz', sa.Float(), nullable=True),
        sa.Column('mx', sa.Float(), nullable=True),
        sa.Column('my', sa.Float(), nullable=True),
        sa.Column('mz', sa.Float(), nullable=True),
        sa.Column('magnitude', sa.Float(), nullable=True),
        sa.Column('direction', sa.String(), nullable=True),
        sa.Column('distribution', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id', 'load_id', name='uq_project_load')
    )
    op.create_index('ix_loads_id', 'loads', ['id'])
    op.create_index('ix_loads_project_id', 'loads', ['project_id'])
    op.create_index('ix_loads_load_case', 'loads', ['load_case'])
    
    # Analysis Results table
    op.create_table(
        'analysis_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('analysis_type', sa.String(), nullable=False),
        sa.Column('load_case', sa.String(), nullable=False),
        sa.Column('results_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_analysis_results_id', 'analysis_results', ['id'])
    op.create_index('ix_analysis_results_project_id', 'analysis_results', ['project_id'])


def downgrade() -> None:
    """Drop all tables"""
    op.drop_index('ix_analysis_results_project_id', table_name='analysis_results')
    op.drop_index('ix_analysis_results_id', table_name='analysis_results')
    op.drop_table('analysis_results')
    
    op.drop_index('ix_loads_load_case', table_name='loads')
    op.drop_index('ix_loads_project_id', table_name='loads')
    op.drop_index('ix_loads_id', table_name='loads')
    op.drop_table('loads')
    
    op.drop_index('ix_sections_project_id', table_name='sections')
    op.drop_index('ix_sections_id', table_name='sections')
    op.drop_table('sections')
    
    op.drop_index('ix_materials_project_id', table_name='materials')
    op.drop_index('ix_materials_id', table_name='materials')
    op.drop_table('materials')
    
    op.drop_index('ix_elements_project_id', table_name='elements')
    op.drop_index('ix_elements_id', table_name='elements')
    op.drop_table('elements')
    
    op.drop_index('ix_nodes_project_id', table_name='nodes')
    op.drop_index('ix_nodes_id', table_name='nodes')
    op.drop_table('nodes')
    
    op.drop_index('ix_projects_id', table_name='projects')
    op.drop_table('projects')
