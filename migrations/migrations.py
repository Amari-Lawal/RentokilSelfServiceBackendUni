import os
import psycopg2


def run_migrations():
    conn = psycopg2.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
    )

    cur = conn.cursor()
    print("Running migrations...")

    cur.execute("""
-- =========================================
-- Enable UUID extension
-- =========================================
create extension if not exists "uuid-ossp";


-- =========================================
-- Drop tables (for dev reset)
-- =========================================
drop table if exists organisation_admin cascade;
drop table if exists user_roles cascade;
drop table if exists members cascade;
drop table if exists operators cascade;
drop table if exists organisations cascade;
drop table if exists roles cascade;


-- =========================================
-- ROLES
-- =========================================
create table roles (
    id uuid primary key,
    name text not null unique
);

insert into roles (id, name) values
(uuid_generate_v5(uuid_nil(), 'member'), 'member'),
(uuid_generate_v5(uuid_nil(), 'parent'), 'parent'),
(uuid_generate_v5(uuid_nil(), 'operator'), 'operator'),
(uuid_generate_v5(uuid_nil(), 'organisation_admin'), 'organisation_admin');


-- =========================================
-- ORGANISATIONS
-- =========================================
create table organisations (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    created_at timestamptz default now()
);


-- =========================================
-- ORG ADMINS
-- =========================================
create table organisation_admin (
    id uuid primary key
        references auth.users(id)
        on delete cascade,
    organisation_id uuid not null
        references organisations(id)
        on delete cascade,
    created_at timestamptz default now()
);

create index idx_organisation_admin_org
on organisation_admin(organisation_id);


-- =========================================
-- OPERATORS
-- =========================================
create table operators (
    id uuid primary key
        references auth.users(id)
        on delete cascade,
    username text not null,
    organisation_id uuid not null
        references organisations(id)
        on delete cascade,

    created_at timestamptz default now(),

    -- required for composite FK from members
    unique (id, organisation_id)
);

create index idx_operator_org
on operators(organisation_id);


-- =========================================
-- MEMBERS
-- =========================================
create table members (
    id uuid primary key
        references auth.users(id)
        on delete cascade,

    operator_id uuid not null,
    organisation_id uuid not null,

    username text not null unique,
    first_name text not null,
    created_at timestamptz default now(),

    -- enforce same organisation as operator
    foreign key (operator_id, organisation_id)
        references operators(id, organisation_id)
        on delete cascade
);

create index idx_member_operator
on members(operator_id);

create index idx_member_org
on members(organisation_id);


-- =========================================
-- USER ROLES (SCOPED TO ORGANISATION)
-- =========================================
create table user_roles (
    user_id uuid
        references auth.users(id)
        on delete cascade,

    role_id uuid
        references roles(id)
        on delete cascade,

    organisation_id uuid
        references organisations(id)
        on delete cascade,

    primary key (user_id, role_id, organisation_id)
);

create index idx_user_roles_user
on user_roles(user_id);

create index idx_user_roles_role
on user_roles(role_id);

create index idx_user_roles_org
on user_roles(organisation_id);
                
-- =========================================
-- RLS Policies
-- =========================================
CREATE POLICY "Enable read access for public (full table scan)"
ON public.organisations
AS PERMISSIVE
FOR SELECT
TO public -- service_role
USING (true);
create policy "Enable read access for all users"
ON "public"."user_roles"
AS PERMISSIVE
FOR SELECT
TO public -- service_role
USING (
  true
);     

CREATE POLICY "Enable read access for all users"
ON public.organisation_admin
AS PERMISSIVE
FOR SELECT
TO public
USING (true);

ALTER table public.user_roles enable row level security;    
alter table public.organisations enable row level security;       
alter table public.organisation_admin enable row level security;

    """)

    print("Migrations completed successfully.")

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    run_migrations()
