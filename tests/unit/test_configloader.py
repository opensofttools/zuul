# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import textwrap

from tests.base import ZuulTestCase


class TenantParserTestCase(ZuulTestCase):
    create_project_keys = True

    CONFIG_SET = set(['pipeline', 'job', 'semaphore', 'project',
                      'project-template', 'nodeset', 'secret'])
    UNTRUSTED_SET = CONFIG_SET - set(['pipeline'])

    def setupAllProjectKeys(self):
        for project in ['common-config', 'org/project1', 'org/project2']:
            self.setupProjectKeys('gerrit', project)


class TestTenantSimple(TenantParserTestCase):
    tenant_config_file = 'config/tenant-parser/simple.yaml'

    def test_tenant_simple(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertEqual(['common-config'],
                         [x.name for x in tenant.config_projects])
        self.assertEqual(['org/project1', 'org/project2'],
                         [x.name for x in tenant.untrusted_projects])
        self.assertEqual(self.CONFIG_SET,
                         tenant.config_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET,
                         tenant.untrusted_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET,
                         tenant.untrusted_projects[1].load_classes)
        self.assertTrue('common-config-job' in tenant.layout.jobs)
        self.assertTrue('project1-job' in tenant.layout.jobs)
        self.assertTrue('project2-job' in tenant.layout.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertTrue('common-config-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        self.assertTrue('project1-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        project2_config = tenant.layout.project_configs.get(
            'review.example.com/org/project2')
        self.assertTrue('common-config-job' in
                        project2_config.pipelines['check'].job_list.jobs)
        self.assertTrue('project2-job' in
                        project2_config.pipelines['check'].job_list.jobs)


class TestTenantOverride(TenantParserTestCase):
    tenant_config_file = 'config/tenant-parser/override.yaml'

    def test_tenant_override(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertEqual(['common-config'],
                         [x.name for x in tenant.config_projects])
        self.assertEqual(['org/project1', 'org/project2'],
                         [x.name for x in tenant.untrusted_projects])
        self.assertEqual(self.CONFIG_SET,
                         tenant.config_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET - set(['project']),
                         tenant.untrusted_projects[0].load_classes)
        self.assertEqual(set(['job']),
                         tenant.untrusted_projects[1].load_classes)
        self.assertTrue('common-config-job' in tenant.layout.jobs)
        self.assertTrue('project1-job' in tenant.layout.jobs)
        self.assertTrue('project2-job' in tenant.layout.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertTrue('common-config-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project1-job' in
                         project1_config.pipelines['check'].job_list.jobs)
        project2_config = tenant.layout.project_configs.get(
            'review.example.com/org/project2')
        self.assertTrue('common-config-job' in
                        project2_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project2-job' in
                         project2_config.pipelines['check'].job_list.jobs)


class TestTenantGroups(TenantParserTestCase):
    tenant_config_file = 'config/tenant-parser/groups.yaml'

    def test_tenant_groups(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertEqual(['common-config'],
                         [x.name for x in tenant.config_projects])
        self.assertEqual(['org/project1', 'org/project2'],
                         [x.name for x in tenant.untrusted_projects])
        self.assertEqual(self.CONFIG_SET,
                         tenant.config_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET - set(['project']),
                         tenant.untrusted_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET - set(['project']),
                         tenant.untrusted_projects[1].load_classes)
        self.assertTrue('common-config-job' in tenant.layout.jobs)
        self.assertTrue('project1-job' in tenant.layout.jobs)
        self.assertTrue('project2-job' in tenant.layout.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertTrue('common-config-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project1-job' in
                         project1_config.pipelines['check'].job_list.jobs)
        project2_config = tenant.layout.project_configs.get(
            'review.example.com/org/project2')
        self.assertTrue('common-config-job' in
                        project2_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project2-job' in
                         project2_config.pipelines['check'].job_list.jobs)


class TestTenantGroups2(TenantParserTestCase):
    tenant_config_file = 'config/tenant-parser/groups2.yaml'

    def test_tenant_groups2(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertEqual(['common-config'],
                         [x.name for x in tenant.config_projects])
        self.assertEqual(['org/project1', 'org/project2'],
                         [x.name for x in tenant.untrusted_projects])
        self.assertEqual(self.CONFIG_SET,
                         tenant.config_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET - set(['project']),
                         tenant.untrusted_projects[0].load_classes)
        self.assertEqual(self.UNTRUSTED_SET - set(['project', 'job']),
                         tenant.untrusted_projects[1].load_classes)
        self.assertTrue('common-config-job' in tenant.layout.jobs)
        self.assertTrue('project1-job' in tenant.layout.jobs)
        self.assertFalse('project2-job' in tenant.layout.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertTrue('common-config-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project1-job' in
                         project1_config.pipelines['check'].job_list.jobs)
        project2_config = tenant.layout.project_configs.get(
            'review.example.com/org/project2')
        self.assertTrue('common-config-job' in
                        project2_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project2-job' in
                         project2_config.pipelines['check'].job_list.jobs)


class TestTenantGroups3(TenantParserTestCase):
    tenant_config_file = 'config/tenant-parser/groups3.yaml'

    def test_tenant_groups3(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertEqual(['common-config'],
                         [x.name for x in tenant.config_projects])
        self.assertEqual(['org/project1', 'org/project2'],
                         [x.name for x in tenant.untrusted_projects])
        self.assertEqual(self.CONFIG_SET,
                         tenant.config_projects[0].load_classes)
        self.assertEqual(set(['job']),
                         tenant.untrusted_projects[0].load_classes)
        self.assertEqual(set(['project', 'job']),
                         tenant.untrusted_projects[1].load_classes)
        self.assertTrue('common-config-job' in tenant.layout.jobs)
        self.assertTrue('project1-job' in tenant.layout.jobs)
        self.assertTrue('project2-job' in tenant.layout.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertTrue('common-config-job' in
                        project1_config.pipelines['check'].job_list.jobs)
        self.assertFalse('project1-job' in
                         project1_config.pipelines['check'].job_list.jobs)
        project2_config = tenant.layout.project_configs.get(
            'review.example.com/org/project2')
        self.assertTrue('common-config-job' in
                        project2_config.pipelines['check'].job_list.jobs)
        self.assertTrue('project2-job' in
                        project2_config.pipelines['check'].job_list.jobs)


class TestSplitConfig(ZuulTestCase):
    tenant_config_file = 'config/split-config/main.yaml'

    def setup_config(self):
        super(TestSplitConfig, self).setup_config()

    def test_split_config(self):
        tenant = self.sched.abide.tenants.get('tenant-one')
        self.assertIn('project-test1', tenant.layout.jobs)
        project_config = tenant.layout.project_configs.get(
            'review.example.com/org/project')
        self.assertIn('project-test1',
                      project_config.pipelines['check'].job_list.jobs)
        project1_config = tenant.layout.project_configs.get(
            'review.example.com/org/project1')
        self.assertIn('project1-project2-integration',
                      project1_config.pipelines['check'].job_list.jobs)

    def test_dynamic_split_config(self):
        in_repo_conf = textwrap.dedent(
            """
            - project:
                name: org/project1
                check:
                  jobs:
                    - project-test1
            """)
        file_dict = {'.zuul.d/gate.yaml': in_repo_conf}
        A = self.fake_gerrit.addFakeChange('org/project1', 'master', 'A',
                                           files=file_dict)
        self.fake_gerrit.addEvent(A.getPatchsetCreatedEvent(1))
        self.waitUntilSettled()
        # project1-project2-integration test removed, only want project-test1
        self.assertHistory([
            dict(name='project-test1', result='SUCCESS', changes='1,1')])
