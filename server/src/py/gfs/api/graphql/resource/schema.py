
# 
# Copyright (c) 2020, John Grundback
# All rights reserved.
# 

import logging

from inspect import Signature, Parameter

from rx.subjects import Subject

import graphql

from gfs.api.graphql.resource.dynamic import GFSGQLDynamicObjectType



source_schema = """

schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type ComposeGQLType {
  id: String
  uuid: String
  created: String
  modified: String
  name: String
  compose: String
  format: String
}

type CreateCompose {
  ok: Boolean
  error: String
  instance: ComposeGQLType
}

type CreateQuery {
  ok: Boolean
  error: String
  instance: QueryGQLType
}

type CreateTemplate {
  ok: Boolean
  error: String
  instance: TemplateGQLType
}

type CreateType {
  ok: Boolean
  error: String
  instance: TypeSchema
}

type DHCPService {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: Machine
  description: String
  name: String
  subnets: [Subnet]
  defaultLeaseTime: String
  options: [DHCPServiceOption]
  hosts: [MachineGroup]
  maxLeaseTime: String
  aliases: [MachineAliasGroup]
  resolvers: [RemoteHostGroup]
  deployed: [Ip]
}

type DHCPServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DHCPService
}

type DHCPServiceOption {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  value: String
  name: String
}

type DHCPServiceOptionEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DHCPServiceOption
}

input DHCPServiceOptionInput {
  id: String
  uuid: String
  tags: [String]
  value: String!
  name: String!
}

type DHCPServiceSubnet {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  netmask: Ip
  rangeEnd: Ip
  routes: [Ip]
  network: Ip
  nextServer: Ip
  description: String
  rangeStart: Ip
  resolvers: [Ip]
  routers: [Ip]
  name: String
  options: [DHCPServiceOption]
}

type DHCPServiceSubnetEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DHCPServiceSubnet
}

type DNSBINDService {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: Machine
  description: String
  name: String
  subnets: [Subnet]
  hosts: [MachineGroup]
  aliases: [MachineAliasGroup]
  resolvers: [RemoteHostGroup]
  deployed: [Machine]
}

type DNSBINDServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DNSBINDService
}

type DNSMasqService {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: Machine
  description: String
  name: String
  subnets: [Subnet]
  hosts: [MachineGroup]
  aliases: [MachineAliasGroup]
  resolvers: [RemoteHostGroup]
  deployed: [Ip]
}

type DNSMasqServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DNSMasqService
}

type DeleteCompose {
  ok: Boolean
  error: String
}

type DeleteQuery {
  ok: Boolean
  error: String
}

type DeleteTemplate {
  ok: Boolean
  error: String
}

type DeleteType {
  ok: Boolean
  error: String
}

type Deployable {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  isDeployed: String
  target: Machine
}

type DeployableEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Deployable
}

type DeployedService {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: Machine
  description: String
  name: String
  path: String
  pcol: String
  host: Machine
  alias: MachineAlias
  port: String
}

type DeployedServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DeployedService
}

type DeployedServiceGroup {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  members: [DeployedService]
  description: String
  name: String
}

type DeployedServiceGroupEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: DeployedServiceGroup
}

input DeployedServiceGroupInput {
  id: String
  uuid: String
  tags: [String]
  members: [DeployedServiceInput]
  addMembers: [TypeRefInput]
  description: String!
  name: String!
}

input DeployedServiceInput {
  id: String
  uuid: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: MachineInput
  setTarget: TypeRefInput
  description: String
  name: String!
  path: String
  pcol: String
  host: MachineInput
  setHost: TypeRefInput
  alias: MachineAliasInput
  setAlias: TypeRefInput
  port: String!
}

type Extends {
  name: String!
  version: Int!
}

input ExtendsInput {
  name: String!
  version: Int = 1
}

type HTTPService {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
  isDeployed: String
  target: Machine
  description: String
  name: String
  services: [DeployedServiceGroup]
  port: String
}

type HTTPServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: HTTPService
}

type Implements {
  name: String!
  version: Int!
}

input ImplementsInput {
  name: String!
  version: Int = 1
}

type Ip {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  description: String
  address: String
  name: String
}

type IpEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Ip
}

input IpInput {
  id: String
  uuid: String
  tags: [String]
  description: String
  address: String!
  name: String!
}

type Machine {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  interface: NetDevice
  release: String
  memory: String
  machine: String
  codename: String
  interfaces: [NetDevice]
  description: String
  system: String
  platform: String
  vendor: String
  version: String
  processor: String
  cores: String
  kernel: String
  cpus: String
  arch: String
  name: String
}

type MachineAlias {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  host: Machine
  description: String
  name: String
}

type MachineAliasEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: MachineAlias
}

type MachineAliasGroup {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  members: [MachineAlias]
  description: String
  name: String
}

type MachineAliasGroupEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: MachineAliasGroup
}

input MachineAliasGroupInput {
  id: String
  uuid: String
  tags: [String]
  members: [MachineAliasInput]
  addMembers: [TypeRefInput]
  description: String!
  name: String!
}

input MachineAliasInput {
  id: String
  uuid: String
  tags: [String]
  host: MachineInput
  setHost: TypeRefInput
  description: String
  name: String
}

type MachineEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Machine
}

type MachineGroup {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  members: [Machine]
  description: String
  name: String
}

type MachineGroupEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: MachineGroup
}

input MachineGroupInput {
  id: String
  uuid: String
  tags: [String]
  members: [MachineInput]
  addMembers: [TypeRefInput]
  description: String!
  name: String!
}

input MachineInput {
  id: String
  uuid: String
  tags: [String]
  interface: NetDeviceInput
  setInterface: TypeRefInput
  release: String!
  memory: String!
  machine: String!
  codename: String!
  interfaces: [NetDeviceInput]
  addInterfaces: [TypeRefInput]
  description: String
  system: String!
  platform: String!
  vendor: String!
  version: String!
  processor: String!
  cores: String!
  kernel: String!
  cpus: String!
  arch: String!
  name: String!
}

type Mutation {
  createQuery(filter: String, name: String!, query: String!): CreateQuery
  updateQuery(filter: String, id: String!, name: String, query: String): UpdateQuery
  deleteQuery(id: String!): DeleteQuery
  createTemplate(format: String, name: String!, template: String!): CreateTemplate
  updateTemplate(format: String, id: String!, name: String, template: String): UpdateTemplate
  deleteTemplate(id: String!): DeleteTemplate
  createType(extends: ExtendsInput, implements: [ImplementsInput], name: String!, properties: [PropertyInput]!, required: [String], type: String! = "object", version: Int = 1): CreateType
  deleteType(name: String!, version: Int): DeleteType
  createCompose(compose: String!, format: String, name: String!): CreateCompose
  updateCompose(compose: String, format: String, id: String!, name: String): UpdateCompose
  deleteCompose(id: String!): DeleteCompose
  createDHCPServiceOption(name: String!, tags: [String], value: String!): createDHCPServiceOption
  updateDHCPServiceOption(id: String!, name: String, tags: [String], value: String): updateDHCPServiceOption
  deleteDHCPServiceOption(id: String!): deleteDHCPServiceOption
  createIp(address: String!, description: String, name: String!, tags: [String]): createIp
  updateIp(address: String, description: String, id: String!, name: String, tags: [String]): updateIp
  deleteIp(id: String!): deleteIp
  createSubnet(addResolvers: [TypeRefInput], addRouters: [TypeRefInput], addRoutes: [TypeRefInput], description: String, name: String, netmask: IpInput, network: IpInput, nextServer: IpInput, rangeEnd: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], routes: [IpInput], setNetmask: TypeRefInput, setNetwork: TypeRefInput, setNextServer: TypeRefInput, setRangeEnd: TypeRefInput, setRangeStart: TypeRefInput, tags: [String]): createSubnet
  updateSubnet(addResolvers: [TypeRefInput], addRouters: [TypeRefInput], addRoutes: [TypeRefInput], delResolvers: [TypeRefInput], delRouters: [TypeRefInput], delRoutes: [TypeRefInput], description: String, id: String!, name: String, netmask: IpInput, network: IpInput, nextServer: IpInput, rangeEnd: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], routes: [IpInput], setNetmask: TypeRefInput, setNetwork: TypeRefInput, setNextServer: TypeRefInput, setRangeEnd: TypeRefInput, setRangeStart: TypeRefInput, tags: [String]): updateSubnet
  deleteSubnet(id: String!): deleteSubnet
  createDHCPServiceSubnet(addOptions: [TypeRefInput], addResolvers: [TypeRefInput], addRouters: [TypeRefInput], addRoutes: [TypeRefInput], description: String, name: String!, netmask: IpInput, network: IpInput, nextServer: IpInput, options: [DHCPServiceOptionInput], rangeEnd: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], routes: [IpInput], setNetmask: TypeRefInput, setNetwork: TypeRefInput, setNextServer: TypeRefInput, setRangeEnd: TypeRefInput, setRangeStart: TypeRefInput, tags: [String]): createDHCPServiceSubnet
  updateDHCPServiceSubnet(addOptions: [TypeRefInput], addResolvers: [TypeRefInput], addRouters: [TypeRefInput], addRoutes: [TypeRefInput], delOptions: [TypeRefInput], delResolvers: [TypeRefInput], delRouters: [TypeRefInput], delRoutes: [TypeRefInput], description: String, id: String!, name: String, netmask: IpInput, network: IpInput, nextServer: IpInput, options: [DHCPServiceOptionInput], rangeEnd: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], routes: [IpInput], setNetmask: TypeRefInput, setNetwork: TypeRefInput, setNextServer: TypeRefInput, setRangeEnd: TypeRefInput, setRangeStart: TypeRefInput, tags: [String]): updateDHCPServiceSubnet
  deleteDHCPServiceSubnet(id: String!): deleteDHCPServiceSubnet
  createNetDevice(addAddresses: [TypeRefInput], addresses: [IpInput], description: String, hwaddr: String!, name: String!, tags: [String]): createNetDevice
  updateNetDevice(addAddresses: [TypeRefInput], addresses: [IpInput], delAddresses: [TypeRefInput], description: String, hwaddr: String, id: String!, name: String, tags: [String]): updateNetDevice
  deleteNetDevice(id: String!): deleteNetDevice
  createMachine(addInterfaces: [TypeRefInput], arch: String!, codename: String!, cores: String!, cpus: String!, description: String, interface: NetDeviceInput, interfaces: [NetDeviceInput], kernel: String!, machine: String!, memory: String!, name: String!, platform: String!, processor: String!, release: String!, setInterface: TypeRefInput, system: String!, tags: [String], vendor: String!, version: String!): createMachine
  updateMachine(addInterfaces: [TypeRefInput], arch: String, codename: String, cores: String, cpus: String, delInterfaces: [TypeRefInput], description: String, id: String!, interface: NetDeviceInput, interfaces: [NetDeviceInput], kernel: String, machine: String, memory: String, name: String, platform: String, processor: String, release: String, setInterface: TypeRefInput, system: String, tags: [String], vendor: String, version: String): updateMachine
  deleteMachine(id: String!): deleteMachine
  createDeployable(isDeployed: String, setTarget: TypeRefInput, tags: [String], target: MachineInput): createDeployable
  updateDeployable(id: String!, isDeployed: String, setTarget: TypeRefInput, tags: [String], target: MachineInput): updateDeployable
  deleteDeployable(id: String!): deleteDeployable
  createMachineAlias(description: String, host: MachineInput, name: String, setHost: TypeRefInput, tags: [String]): createMachineAlias
  updateMachineAlias(description: String, host: MachineInput, id: String!, name: String, setHost: TypeRefInput, tags: [String]): updateMachineAlias
  deleteMachineAlias(id: String!): deleteMachineAlias
  createMachineAliasGroup(addMembers: [TypeRefInput], description: String!, members: [MachineAliasInput], name: String!, tags: [String]): createMachineAliasGroup
  updateMachineAliasGroup(addMembers: [TypeRefInput], delMembers: [TypeRefInput], description: String, id: String!, members: [MachineAliasInput], name: String, tags: [String]): updateMachineAliasGroup
  deleteMachineAliasGroup(id: String!): deleteMachineAliasGroup
  createMachineGroup(addMembers: [TypeRefInput], description: String!, members: [MachineInput], name: String!, tags: [String]): createMachineGroup
  updateMachineGroup(addMembers: [TypeRefInput], delMembers: [TypeRefInput], description: String, id: String!, members: [MachineInput], name: String, tags: [String]): updateMachineGroup
  deleteMachineGroup(id: String!): deleteMachineGroup
  createRemoteHost(addAddresses: [TypeRefInput], addresses: [IpInput], description: String!, name: String!, tags: [String]): createRemoteHost
  updateRemoteHost(addAddresses: [TypeRefInput], addresses: [IpInput], delAddresses: [TypeRefInput], description: String, id: String!, name: String, tags: [String]): updateRemoteHost
  deleteRemoteHost(id: String!): deleteRemoteHost
  createRemoteHostGroup(addMembers: [TypeRefInput], description: String!, members: [RemoteHostInput], name: String!, tags: [String]): createRemoteHostGroup
  updateRemoteHostGroup(addMembers: [TypeRefInput], delMembers: [TypeRefInput], description: String, id: String!, members: [RemoteHostInput], name: String, tags: [String]): updateRemoteHostGroup
  deleteRemoteHostGroup(id: String!): deleteRemoteHostGroup
  createRunnable(isRunning: String, status: String, tags: [String]): createRunnable
  updateRunnable(id: String!, isRunning: String, status: String, tags: [String]): updateRunnable
  deleteRunnable(id: String!): deleteRunnable
  createService(description: String, name: String!, tags: [String]): createService
  updateService(description: String, id: String!, name: String, tags: [String]): updateService
  deleteService(id: String!): deleteService
  createDHCPService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addOptions: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], defaultLeaseTime: String!, deployed: [IpInput], description: String, hosts: [MachineGroupInput], isDeployed: String, isRunning: String, maxLeaseTime: String!, name: String!, options: [DHCPServiceOptionInput], resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): createDHCPService
  updateDHCPService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addOptions: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], defaultLeaseTime: String, delAliases: [TypeRefInput], delDeployed: [TypeRefInput], delHosts: [TypeRefInput], delOptions: [TypeRefInput], delResolvers: [TypeRefInput], delSubnets: [TypeRefInput], deployed: [IpInput], description: String, hosts: [MachineGroupInput], id: String!, isDeployed: String, isRunning: String, maxLeaseTime: String, name: String, options: [DHCPServiceOptionInput], resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): updateDHCPService
  deleteDHCPService(id: String!): deleteDHCPService
  createDNSBINDService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], deployed: [MachineInput], description: String, hosts: [MachineGroupInput], isDeployed: String, isRunning: String, name: String!, resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): createDNSBINDService
  updateDNSBINDService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], delAliases: [TypeRefInput], delDeployed: [TypeRefInput], delHosts: [TypeRefInput], delResolvers: [TypeRefInput], delSubnets: [TypeRefInput], deployed: [MachineInput], description: String, hosts: [MachineGroupInput], id: String!, isDeployed: String, isRunning: String, name: String, resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): updateDNSBINDService
  deleteDNSBINDService(id: String!): deleteDNSBINDService
  createDNSMasqService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], deployed: [IpInput], description: String, hosts: [MachineGroupInput], isDeployed: String, isRunning: String, name: String!, resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): createDNSMasqService
  updateDNSMasqService(addAliases: [TypeRefInput], addDeployed: [TypeRefInput], addHosts: [TypeRefInput], addResolvers: [TypeRefInput], addSubnets: [TypeRefInput], aliases: [MachineAliasGroupInput], delAliases: [TypeRefInput], delDeployed: [TypeRefInput], delHosts: [TypeRefInput], delResolvers: [TypeRefInput], delSubnets: [TypeRefInput], deployed: [IpInput], description: String, hosts: [MachineGroupInput], id: String!, isDeployed: String, isRunning: String, name: String, resolvers: [RemoteHostGroupInput], setTarget: TypeRefInput, status: String, subnets: [SubnetInput], tags: [String], target: MachineInput): updateDNSMasqService
  deleteDNSMasqService(id: String!): deleteDNSMasqService
  createDeployedService(alias: MachineAliasInput, description: String, host: MachineInput, isDeployed: String, isRunning: String, name: String!, path: String, pcol: String, port: String!, setAlias: TypeRefInput, setHost: TypeRefInput, setTarget: TypeRefInput, status: String, tags: [String], target: MachineInput): createDeployedService
  updateDeployedService(alias: MachineAliasInput, description: String, host: MachineInput, id: String!, isDeployed: String, isRunning: String, name: String, path: String, pcol: String, port: String, setAlias: TypeRefInput, setHost: TypeRefInput, setTarget: TypeRefInput, status: String, tags: [String], target: MachineInput): updateDeployedService
  deleteDeployedService(id: String!): deleteDeployedService
  createDeployedServiceGroup(addMembers: [TypeRefInput], description: String!, members: [DeployedServiceInput], name: String!, tags: [String]): createDeployedServiceGroup
  updateDeployedServiceGroup(addMembers: [TypeRefInput], delMembers: [TypeRefInput], description: String, id: String!, members: [DeployedServiceInput], name: String, tags: [String]): updateDeployedServiceGroup
  deleteDeployedServiceGroup(id: String!): deleteDeployedServiceGroup
  createHTTPService(addServices: [TypeRefInput], description: String, isDeployed: String, isRunning: String, name: String!, port: String!, services: [DeployedServiceGroupInput], setTarget: TypeRefInput, status: String, tags: [String], target: MachineInput): createHTTPService
  updateHTTPService(addServices: [TypeRefInput], delServices: [TypeRefInput], description: String, id: String!, isDeployed: String, isRunning: String, name: String, port: String, services: [DeployedServiceGroupInput], setTarget: TypeRefInput, status: String, tags: [String], target: MachineInput): updateHTTPService
  deleteHTTPService(id: String!): deleteHTTPService
  createServiceGroup(addMembers: [TypeRefInput], description: String!, members: [ServiceInput], name: String!, tags: [String]): createServiceGroup
  updateServiceGroup(addMembers: [TypeRefInput], delMembers: [TypeRefInput], description: String, id: String!, members: [ServiceInput], name: String, tags: [String]): updateServiceGroup
  deleteServiceGroup(id: String!): deleteServiceGroup
}

type NetDevice {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  hwaddr: String
  description: String
  name: String
  addresses: [Ip]
}

type NetDeviceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: NetDevice
}

input NetDeviceInput {
  id: String
  uuid: String
  tags: [String]
  hwaddr: String!
  description: String
  name: String!
  addresses: [IpInput]
  addAddresses: [TypeRefInput]
}

type Property {
  name: String
  type: String
  title: String
  itemsref: String
}

input PropertyInput {
  name: String!
  type: String! = "string"
  title: String
  itemsref: String
}

type Query {
  query(id: String!): QueryGQLType
  queries(name: String): [QueryGQLType]
  querys(name: String): [QueryGQLType]
  template(id: String!): TemplateGQLType
  templates(name: String): [TemplateGQLType]
  type(name: String!, version: Int): TypeSchema
  types(name: String, version: Int): [TypeSchema]
  compose(name: String!): ComposeGQLType
  composes(name: String): [ComposeGQLType]
  DHCPServiceOptions(value: String, name: String, tags: [String]): [DHCPServiceOption]
  DHCPServiceOption(id: String!): DHCPServiceOption
  Ips(address: String, name: String, tags: [String]): [Ip]
  Ip(id: String!): Ip
  Subnets(netmask: IpInput, rangeEnd: IpInput, routes: [IpInput], network: IpInput, nextServer: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], name: String, tags: [String]): [Subnet]
  Subnet(id: String!): Subnet
  DHCPServiceSubnets(netmask: IpInput, rangeEnd: IpInput, routes: [IpInput], network: IpInput, nextServer: IpInput, rangeStart: IpInput, resolvers: [IpInput], routers: [IpInput], name: String, options: [DHCPServiceOptionInput], tags: [String]): [DHCPServiceSubnet]
  DHCPServiceSubnet(id: String!): DHCPServiceSubnet
  NetDevices(hwaddr: String, name: String, addresses: [IpInput], tags: [String]): [NetDevice]
  NetDevice(id: String!): NetDevice
  Machines(interface: NetDeviceInput, release: String, memory: String, machine: String, codename: String, interfaces: [NetDeviceInput], system: String, platform: String, vendor: String, version: String, processor: String, cores: String, kernel: String, cpus: String, arch: String, name: String, tags: [String]): [Machine]
  Machine(id: String!): Machine
  Deployables(isDeployed: String, target: MachineInput, tags: [String]): [Deployable]
  Deployable(id: String!): Deployable
  MachineAliass(host: MachineInput, name: String, tags: [String]): [MachineAlias]
  MachineAlias(id: String!): MachineAlias
  MachineAliasGroups(members: [MachineAliasInput], name: String, tags: [String]): [MachineAliasGroup]
  MachineAliasGroup(id: String!): MachineAliasGroup
  MachineGroups(members: [MachineInput], name: String, tags: [String]): [MachineGroup]
  MachineGroup(id: String!): MachineGroup
  RemoteHosts(name: String, addresses: [IpInput], tags: [String]): [RemoteHost]
  RemoteHost(id: String!): RemoteHost
  RemoteHostGroups(members: [RemoteHostInput], name: String, tags: [String]): [RemoteHostGroup]
  RemoteHostGroup(id: String!): RemoteHostGroup
  Runnables(status: String, isRunning: String, tags: [String]): [Runnable]
  Runnable(id: String!): Runnable
  Services(name: String, tags: [String]): [Service]
  Service(id: String!): Service
  DHCPServices(status: String, isRunning: String, isDeployed: String, target: MachineInput, name: String, subnets: [SubnetInput], defaultLeaseTime: String, options: [DHCPServiceOptionInput], hosts: [MachineGroupInput], maxLeaseTime: String, aliases: [MachineAliasGroupInput], resolvers: [RemoteHostGroupInput], deployed: [IpInput], tags: [String]): [DHCPService]
  DHCPService(id: String!): DHCPService
  DNSBINDServices(status: String, isRunning: String, isDeployed: String, target: MachineInput, name: String, subnets: [SubnetInput], hosts: [MachineGroupInput], aliases: [MachineAliasGroupInput], resolvers: [RemoteHostGroupInput], deployed: [MachineInput], tags: [String]): [DNSBINDService]
  DNSBINDService(id: String!): DNSBINDService
  DNSMasqServices(status: String, isRunning: String, isDeployed: String, target: MachineInput, name: String, subnets: [SubnetInput], hosts: [MachineGroupInput], aliases: [MachineAliasGroupInput], resolvers: [RemoteHostGroupInput], deployed: [IpInput], tags: [String]): [DNSMasqService]
  DNSMasqService(id: String!): DNSMasqService
  DeployedServices(status: String, isRunning: String, isDeployed: String, target: MachineInput, name: String, path: String, pcol: String, host: MachineInput, alias: MachineAliasInput, port: String, tags: [String]): [DeployedService]
  DeployedService(id: String!): DeployedService
  DeployedServiceGroups(members: [DeployedServiceInput], name: String, tags: [String]): [DeployedServiceGroup]
  DeployedServiceGroup(id: String!): DeployedServiceGroup
  HTTPServices(status: String, isRunning: String, isDeployed: String, target: MachineInput, name: String, services: [DeployedServiceGroupInput], port: String, tags: [String]): [HTTPService]
  HTTPService(id: String!): HTTPService
  ServiceGroups(members: [ServiceInput], name: String, tags: [String]): [ServiceGroup]
  ServiceGroup(id: String!): ServiceGroup
}

type QueryGQLType {
  id: String
  uuid: String
  created: String
  modified: String
  name: String
  query: String
  filter: String
}

type RemoteHost {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  description: String
  name: String
  addresses: [Ip]
}

type RemoteHostEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: RemoteHost
}

type RemoteHostGroup {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  members: [RemoteHost]
  description: String
  name: String
}

type RemoteHostGroupEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: RemoteHostGroup
}

input RemoteHostGroupInput {
  id: String
  uuid: String
  tags: [String]
  members: [RemoteHostInput]
  addMembers: [TypeRefInput]
  description: String!
  name: String!
}

input RemoteHostInput {
  id: String
  uuid: String
  tags: [String]
  description: String!
  name: String!
  addresses: [IpInput]
  addAddresses: [TypeRefInput]
}

type Runnable {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  status: String
  isRunning: String
}

type RunnableEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Runnable
}

type Service {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  description: String
  name: String
}

type ServiceEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Service
}

type ServiceGroup {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  members: [Service]
  description: String
  name: String
}

type ServiceGroupEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: ServiceGroup
}

input ServiceInput {
  id: String
  uuid: String
  tags: [String]
  description: String
  name: String!
}

type Subnet {
  id: String
  uuid: String
  created: String
  modified: String
  tags: [String]
  netmask: Ip
  rangeEnd: Ip
  routes: [Ip]
  network: Ip
  nextServer: Ip
  description: String
  rangeStart: Ip
  resolvers: [Ip]
  routers: [Ip]
  name: String
}

type SubnetEvent {
  event: String
  id: String
  label: String
  sourceid: String
  sourcelabel: String
  targetid: String
  targetlabel: String
  chain: [String]
  node: Subnet
}

input SubnetInput {
  id: String
  uuid: String
  tags: [String]
  netmask: IpInput
  setNetmask: TypeRefInput
  rangeEnd: IpInput
  setRangeEnd: TypeRefInput
  routes: [IpInput]
  addRoutes: [TypeRefInput]
  network: IpInput
  setNetwork: TypeRefInput
  nextServer: IpInput
  setNextServer: TypeRefInput
  description: String
  rangeStart: IpInput
  setRangeStart: TypeRefInput
  resolvers: [IpInput]
  addResolvers: [TypeRefInput]
  routers: [IpInput]
  addRouters: [TypeRefInput]
  name: String
}

type Subscription {
  DHCPServiceOption(events: [String], chain: [String]): DHCPServiceOptionEvent
  Ip(events: [String], chain: [String]): IpEvent
  Subnet(events: [String], chain: [String]): SubnetEvent
  DHCPServiceSubnet(events: [String], chain: [String]): DHCPServiceSubnetEvent
  NetDevice(events: [String], chain: [String]): NetDeviceEvent
  Machine(events: [String], chain: [String]): MachineEvent
  Deployable(events: [String], chain: [String]): DeployableEvent
  MachineAlias(events: [String], chain: [String]): MachineAliasEvent
  MachineAliasGroup(events: [String], chain: [String]): MachineAliasGroupEvent
  MachineGroup(events: [String], chain: [String]): MachineGroupEvent
  RemoteHost(events: [String], chain: [String]): RemoteHostEvent
  RemoteHostGroup(events: [String], chain: [String]): RemoteHostGroupEvent
  Runnable(events: [String], chain: [String]): RunnableEvent
  Service(events: [String], chain: [String]): ServiceEvent
  DHCPService(events: [String], chain: [String]): DHCPServiceEvent
  DNSBINDService(events: [String], chain: [String]): DNSBINDServiceEvent
  DNSMasqService(events: [String], chain: [String]): DNSMasqServiceEvent
  DeployedService(events: [String], chain: [String]): DeployedServiceEvent
  DeployedServiceGroup(events: [String], chain: [String]): DeployedServiceGroupEvent
  HTTPService(events: [String], chain: [String]): HTTPServiceEvent
  ServiceGroup(events: [String], chain: [String]): ServiceGroupEvent
}

type TemplateGQLType {
  id: String
  uuid: String
  created: String
  modified: String
  name: String
  template: String
  format: String
}

input TypeRefInput {
  id: String
}

type TypeSchema {
  id: String
  name: String
  type: String
  version: Int
  extends: Extends
  implements: [Implements]
  typelabel: String
  required: [String]
  properties: [Property]
}

type UpdateCompose {
  ok: Boolean
  error: String
  instance: ComposeGQLType
}

type UpdateQuery {
  ok: Boolean
  error: String
  instance: QueryGQLType
}

type UpdateTemplate {
  ok: Boolean
  error: String
  instance: TemplateGQLType
}

type createDHCPService {
  ok: Boolean
  error: String
  instance: DHCPService
}

type createDHCPServiceOption {
  ok: Boolean
  error: String
  instance: DHCPServiceOption
}

type createDHCPServiceSubnet {
  ok: Boolean
  error: String
  instance: DHCPServiceSubnet
}

type createDNSBINDService {
  ok: Boolean
  error: String
  instance: DNSBINDService
}

type createDNSMasqService {
  ok: Boolean
  error: String
  instance: DNSMasqService
}

type createDeployable {
  ok: Boolean
  error: String
  instance: Deployable
}

type createDeployedService {
  ok: Boolean
  error: String
  instance: DeployedService
}

type createDeployedServiceGroup {
  ok: Boolean
  error: String
  instance: DeployedServiceGroup
}

type createHTTPService {
  ok: Boolean
  error: String
  instance: HTTPService
}

type createIp {
  ok: Boolean
  error: String
  instance: Ip
}

type createMachine {
  ok: Boolean
  error: String
  instance: Machine
}

type createMachineAlias {
  ok: Boolean
  error: String
  instance: MachineAlias
}

type createMachineAliasGroup {
  ok: Boolean
  error: String
  instance: MachineAliasGroup
}

type createMachineGroup {
  ok: Boolean
  error: String
  instance: MachineGroup
}

type createNetDevice {
  ok: Boolean
  error: String
  instance: NetDevice
}

type createRemoteHost {
  ok: Boolean
  error: String
  instance: RemoteHost
}

type createRemoteHostGroup {
  ok: Boolean
  error: String
  instance: RemoteHostGroup
}

type createRunnable {
  ok: Boolean
  error: String
  instance: Runnable
}

type createService {
  ok: Boolean
  error: String
  instance: Service
}

type createServiceGroup {
  ok: Boolean
  error: String
  instance: ServiceGroup
}

type createSubnet {
  ok: Boolean
  error: String
  instance: Subnet
}

type deleteDHCPService {
  ok: Boolean
  error: String
}

type deleteDHCPServiceOption {
  ok: Boolean
  error: String
}

type deleteDHCPServiceSubnet {
  ok: Boolean
  error: String
}

type deleteDNSBINDService {
  ok: Boolean
  error: String
}

type deleteDNSMasqService {
  ok: Boolean
  error: String
}

type deleteDeployable {
  ok: Boolean
  error: String
}

type deleteDeployedService {
  ok: Boolean
  error: String
}

type deleteDeployedServiceGroup {
  ok: Boolean
  error: String
}

type deleteHTTPService {
  ok: Boolean
  error: String
}

type deleteIp {
  ok: Boolean
  error: String
}

type deleteMachine {
  ok: Boolean
  error: String
}

type deleteMachineAlias {
  ok: Boolean
  error: String
}

type deleteMachineAliasGroup {
  ok: Boolean
  error: String
}

type deleteMachineGroup {
  ok: Boolean
  error: String
}

type deleteNetDevice {
  ok: Boolean
  error: String
}

type deleteRemoteHost {
  ok: Boolean
  error: String
}

type deleteRemoteHostGroup {
  ok: Boolean
  error: String
}

type deleteRunnable {
  ok: Boolean
  error: String
}

type deleteService {
  ok: Boolean
  error: String
}

type deleteServiceGroup {
  ok: Boolean
  error: String
}

type deleteSubnet {
  ok: Boolean
  error: String
}

type updateDHCPService {
  ok: Boolean
  error: String
  instance: DHCPService
}

type updateDHCPServiceOption {
  ok: Boolean
  error: String
  instance: DHCPServiceOption
}

type updateDHCPServiceSubnet {
  ok: Boolean
  error: String
  instance: DHCPServiceSubnet
}

type updateDNSBINDService {
  ok: Boolean
  error: String
  instance: DNSBINDService
}

type updateDNSMasqService {
  ok: Boolean
  error: String
  instance: DNSMasqService
}

type updateDeployable {
  ok: Boolean
  error: String
  instance: Deployable
}

type updateDeployedService {
  ok: Boolean
  error: String
  instance: DeployedService
}

type updateDeployedServiceGroup {
  ok: Boolean
  error: String
  instance: DeployedServiceGroup
}

type updateHTTPService {
  ok: Boolean
  error: String
  instance: HTTPService
}

type updateIp {
  ok: Boolean
  error: String
  instance: Ip
}

type updateMachine {
  ok: Boolean
  error: String
  instance: Machine
}

type updateMachineAlias {
  ok: Boolean
  error: String
  instance: MachineAlias
}

type updateMachineAliasGroup {
  ok: Boolean
  error: String
  instance: MachineAliasGroup
}

type updateMachineGroup {
  ok: Boolean
  error: String
  instance: MachineGroup
}

type updateNetDevice {
  ok: Boolean
  error: String
  instance: NetDevice
}

type updateRemoteHost {
  ok: Boolean
  error: String
  instance: RemoteHost
}

type updateRemoteHostGroup {
  ok: Boolean
  error: String
  instance: RemoteHostGroup
}

type updateRunnable {
  ok: Boolean
  error: String
  instance: Runnable
}

type updateService {
  ok: Boolean
  error: String
  instance: Service
}

type updateServiceGroup {
  ok: Boolean
  error: String
  instance: ServiceGroup
}

type updateSubnet {
  ok: Boolean
  error: String
  instance: Subnet
}

"""



# # def subscription_dhcpservice_resolver(value, info, **args):
# def subscription_resolver(value, info, **args):
#     schemas = GFSGQLSchemas.instance()
#     namespace = None
#     label = None
#     subject = schemas.subject(namespace, label)
#     return subject



# class GFSGQLSchemas():
class GFSGQLSchemas(GFSGQLDynamicObjectType):

    __instance = None

    _subject = Subject()

    @classmethod
    def instance(clazz):
        if not GFSGQLSchemas.__instance:
            GFSGQLSchemas.__instance = GFSGQLSchemas()
        return GFSGQLSchemas.__instance

    # @classmethod
    # def subscription_resolver(clazz, value, info, **args):
    #   print("GFSGQLSchemas subscription_resolver")
    #   print(value)
    #   print(info)
    #   schemas = GFSGQLSchemas.instance()
    #   namespace = "gfs1"
    #   label = "hello"
    #   subject = schemas.subject(namespace, label)
    #   return subject

    @classmethod
    def makeSubscriptionResolverFunctionSignature(clazz, namespace):

        params = []
        params.append(Parameter("clazz", kind=Parameter.POSITIONAL_OR_KEYWORD))
        params.append(Parameter("value", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("info", kind=Parameter.POSITIONAL_OR_KEYWORD, default=None))

        return params

    @classmethod
    def makeSubscriptionResolverFunction(clazz, namespace, name):

        params = GFSGQLSchemas.makeSubscriptionResolverFunctionSignature(
            namespace
        )
        sig = Signature(params)

        # def resolve(*args, **kwargs):
        #     print("GFSGQLSchemas makeSubscriptionResolverFunction resolve")
        #     print(namespace)
        #     print(name)
        # 
        #     clazz = None
        #     value = None
        #     info = None
        # 
        #     # clazz = args[0]
        #     info = args[1]
        #     # info = args[2]
        # 
        #     fields = GFSGQLSchemas.get_fields(info)
        # 
        #     return GFSGQLSchemas.instance().subject(namespace, name)

        def resolve(*args, **kwargs):
            print("GFSGQLSchemas makeSubscriptionResolverFunction resolve with filter")
            print(namespace)
            print(name)

            root = args[0]
            info = args[1]

            events = None # args[2]
            chain = None # args[3]

            # https://docs.graphene-python.org/projects/django/en/latest/subscriptions/
            # https://pypi.org/project/graphene-subscriptions/
            return GFSGQLSchemas.instance().subject(namespace, name).filter(
                lambda event: 
                    event.get("namespace") == namespace and \
                    event.get("label") == name
                    # (not events or event.get("event") in events) and \
                    # (not chain or ("-".join(event.get("chain", [])).startswith( "-".join(chain))))
            ).map(lambda event: event)

        return GFSGQLSchemas.createFunction('resolve', sig, resolve)

    # 
    # Borrowed from graphql_tools.py
    # def build_executable_schema(schema_definition, resolvers):
    # 
    # build_executable schema
    #
    # accepts schema_definition (string) and resolvers (object) in style of graphql-tools
    # returns a schema ready for execution
    # 
    def build_executable_schema(self, namespace, schema_definition): # , resolvers):
        ast = graphql.parse(schema_definition)
        schema = graphql.build_ast_schema(ast)

        # for typeName in resolvers:
        fieldType = schema.get_type("Subscription")

        # for fieldName in resolvers[typeName]:
        for fieldName in fieldType.fields:
            if fieldType is graphql.GraphQLScalarType:
                # fieldType.fields[fieldName].resolver = resolvers["Subscription"] # resolvers[typeName][fieldName]
                fieldType.fields[fieldName].resolver = GFSGQLSchemas.makeSubscriptionResolverFunction(
                    namespace, 
                    fieldName
                )
                continue

            field = fieldType.fields[fieldName]
            # field.resolver = resolvers["Subscription"] # resolvers[typeName][fieldName]
            field.resolver = GFSGQLSchemas.makeSubscriptionResolverFunction(
                namespace, 
                fieldName
            )

        # if not fieldType.fields: continue

        for remaining in fieldType.fields:
            if not fieldType.fields[remaining].resolver:
                fieldType.fields[remaining].resolver = \
                    lambda value, info, _r=remaining, **args: value[_r]

        return schema

    def schema(self, namespace):
        my_schema = self.build_executable_schema(namespace, source_schema)
        return my_schema

    def subject(self, namespace, name):
        return self._subject
