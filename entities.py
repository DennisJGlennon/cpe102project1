import point
import worldmodel
from actions import *

class Background:
   def __init__(self, name, imgs):
      self.name = name
      self.imgs = imgs
      self.current_img = 0

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_name(self):
      return self.name

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return 'unknown'


class MinerNotFull:
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.animation_rate = animation_rate
      self.pending_actions = []
      
   def get_name(self):
      return self.name
      
   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_rate(self):
      return self.rate
      
   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]
      
   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def get_resource_limit(self):
      return self.resource_limit
      
   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_animation_rate(self):
      return self.animation_rate

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def entity_string(self):
      return ' '.join(['miner', self.name, str(self.position.x),
         str(self.position.y), str(self.resource_limit),
         str(self.rate), str(self.animation_rate)])


   def next_position(self, world, dest_pt): #both miners
      entity_pt = self.get_position()
      horiz = sign(dest_pt.x - entity_pt.x)
      new_pt = point.Point(entity_pt.x + horiz, entity_pt.y)

      if horiz == 0 or world.is_occupied(new_pt):
         vert = sign(dest_pt.y - entity_pt.y)
         new_pt = point.Point(entity_pt.x, entity_pt.y + vert)

         if vert == 0 or world.is_occupied(new_pt):
            new_pt = point.Point(entity_pt.x, entity_pt.y)

      return new_pt

   def miner_to_ore(self, world, ore): #miner not
      entity_pt = self.get_position()
      if not ore:
         return ([entity_pt], False)
      ore_pt = ore.get_position()
      if entity_pt.adjacent(ore_pt):
         self.set_resource_count(
            1 + self.get_resource_count())
         ore.remove_entity(world)
         return ([ore_pt], True)
      else:
         new_pt = self.next_position(world, ore_pt)
         return (world.move_entity(self, new_pt), False)


   def create_miner_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)

         entity_pt = self.get_position()
         ore = world.find_nearest(entity_pt, entities.Ore)
         (tiles, found) = self.miner_to_ore(world, ore)

         new_entity = self
         if found:
            new_entity = self.try_transform_miner(world,
               self.try_transform_miner_not_full)

         schedule_action(world, new_entity,
            new_entity.create_miner_action(world, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action


   def try_transform_miner_not_full(self, world):
      if self.resource_count < self.resource_limit:
         return self
      else:
         new_entity = entities.MinerFull(
            self.get_name(), self.get_resource_limit(),
            self.get_position(), self.get_rate(),
            self.get_images(), self.get_animation_rate())
         return new_entity


   def try_transform_miner(self, world, transform):
      new_entity = transform(world)
      if self != new_entity:
         clear_pending_actions(world, self)
         world.remove_entity_at(self.get_position())
         world.add_entity(new_entity)
         schedule_animation(world, new_entity)
      return new_entity


   def schedule_entity(self, world, ticks, i_store):
      schedule_action(world, self, self.create_miner_action(world, i_store),
         ticks + self.get_rate())
      schedule_animation(world, self)

class MinerFull:
   def __init__(self, name, resource_limit, position, rate, imgs,
      animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = resource_limit
      self.animation_rate = animation_rate
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_count(self):
      return self.resource_count

   def get_resource_limit(self):
      return self.resource_limit

   def get_name(self):
      return self.name

   def get_animation_rate(self):
      return self.animation_rate

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return 'unknown'

   def next_position(self, world, dest_pt): #both miners
      entity_pt = self.get_position()
      horiz = sign(dest_pt.x - entity_pt.x)
      new_pt = point.Point(entity_pt.x + horiz, entity_pt.y)

      if horiz == 0 or world.is_occupied(new_pt):
         vert = sign(dest_pt.y - entity_pt.y)
         new_pt = point.Point(entity_pt.x, entity_pt.y + vert)

         if vert == 0 or world.is_occupied(new_pt):
            new_pt = point.Point(entity_pt.x, entity_pt.y)

      return new_pt


   def miner_to_smith(self, world, smith):
      entity_pt = self.get_position()
      if not smith:
         return ([entity_pt], False)
      smith_pt = smith.get_position()
      if entity_pt.adjacent(smith_pt):
         smith.set_resource_count(
            smith.get_resource_count() +
            self.get_resource_count())
         self.set_resource_count(0)
         return ([], True)
      else:
         new_pt = self.next_position(world, smith_pt)
         return (world.move_entity(self, new_pt), False)


   def create_miner_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)
         entity_pt = self.get_position()
         smith = world.find_nearest(entity_pt, entities.Blacksmith)
         (tiles, found) = self.miner_to_smith(world, smith)
         new_entity = self
         if found:
            new_entity = self.try_transform_miner(world,
            self.try_transform_miner_full)
         schedule_action(world, new_entity,
            new_entity.create_miner_action(world, i_store),
            current_ticks + new_entity.get_rate())
         return tiles
      return action


   def try_transform_miner_full(self, world):
      new_entity = entities.MinerNotFull(
         self.get_name(), self.get_resource_limit(),
         self.get_position(), self.get_rate(),
         self.get_images(), self.get_animation_rate())

      return new_entity

   def try_transform_miner(self, world, transform):
      new_entity = transform(world)
      if self != new_entity:
         clear_pending_actions(world, self)
         world.remove_entity_at(self.get_position())
         world.add_entity(new_entity)
         schedule_animation(world, new_entity)

      return new_entity


class Vein:
   def __init__(self, name, rate, position, imgs, resource_distance=1):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.resource_distance = resource_distance
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_resource_distance(self):
      return self.resource_distance

   def get_name(self):
      return self.name

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self): 
      return ' '.join(['vein', self.name, str(self.position.x),
         str(self.position.y), str(self.rate),
         str(self.resource_distance)])


   def find_open_around(self, world, distance):
      pt = self.get_position()
      for dy in range(-distance, distance + 1):
         for dx in range(-distance, distance + 1):
            new_pt = point.Point(pt.x + dx, pt.y + dy)

            if (world.within_bounds(new_pt) and
               (not world.is_occupied(new_pt))):
               return new_pt

      return None


   def create_vein_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)
         open_pt = self.find_open_around(world,
         self.get_resource_distance())
         if open_pt:
            ore = world.create_ore1(
               "ore - " + self.get_name() + " - " + str(current_ticks),
               open_pt, current_ticks, i_store)
            world.add_entity(ore)
            tiles = [open_pt]
         else:
            tiles = []

         schedule_action(world, self,
            self.create_vein_action(world, i_store),
            current_ticks + self.get_rate())
         return tiles
      return action


   def schedule_entity(self, world, ticks, i_store):
      schedule_action(world, self, self.create_vein_action(world, i_store),
         ticks + self.get_rate())

      
   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      self.clear_pending_actions()
      world.remove_entity(self)

class Ore:
   def __init__(self, name, position, imgs, rate=5000):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.rate = rate
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_name(self):
      return self.name

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self): 
      return ' '.join(['ore', self.name, str(self.position.x),
         str(self.position.y), str(self.rate)])


   def create_ore_transform_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)
         blob = world.create_blob(self.get_name() + " -- blob",
            self.get_position(),
            self.get_rate() // BLOB_RATE_SCALE,
            current_ticks, i_store)

         self.remove_entity(world)
         world.add_entity(blob)

         return [blob.get_position()]
      return action


   def schedule_entity(self, world, ticks, i_store):
      schedule_action(world, self,
         self.create_ore_transform_action(world, i_store),
         ticks + self.get_rate())
      
   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      self.clear_pending_actions()
      world.remove_entity(self)


class Blacksmith:
   def __init__(self, name, position, imgs, resource_limit, rate,
      resource_distance=1):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.resource_limit = resource_limit
      self.resource_count = 0
      self.rate = rate
      self.resource_distance = resource_distance
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_resource_count(self):
      return self.resource_count

   def set_resource_count(self, n):
      self.resource_count = n

   def get_resource_limit(self):
      return self.resource_limit

   def get_resource_distance(self):
      return self.resource_distance

   def get_name(self):
      return self.name

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return ' '.join(['blacksmith', self.name, str(self.position.x),
         str(self.position.y), str(self.resource_limit),
         str(self.rate), str(self.resource_distance)])



class Obstacle:
   def __init__(self, name, position, imgs):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_name(self):
      return self.name

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return ' '.join(['obstacle', self.name, str(self.position.x),
         str(self.position.y)])


class OreBlob:
   def __init__(self, name, position, rate, imgs, animation_rate):
      self.name = name
      self.position = position
      self.rate = rate
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_name(self):
      return self.name

   def get_animation_rate(self):
      return self.animation_rate

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return 'unknown'

   def blob_next_position(self, world, dest_pt):
      entity_pt = self.get_position()
      horiz = sign(dest_pt.x - entity_pt.x)
      new_pt = point.Point(entity_pt.x + horiz, entity_pt.y)

      if horiz == 0 or (world.is_occupied(new_pt) and
         not isinstance(world.get_tile_occupant(new_pt),
         entities.Ore)):
         vert = sign(dest_pt.y - entity_pt.y)
         new_pt = point.Point(entity_pt.x, entity_pt.y + vert)

         if vert == 0 or (world.is_occupied(new_pt) and
            not isinstance(world.get_tile_occupant(new_pt),
            entities.Ore)):
            new_pt = point.Point(entity_pt.x, entity_pt.y)

      return new_pt

   def blob_to_vein(self, world, vein):
      entity_pt = self.get_position()
      if not vein:
         return ([entity_pt], False)
      vein_pt = vein.get_position()
      if entity_pt.adjacent(vein_pt):
         vein.remove_entity(world)
         return ([vein_pt], True)
      else:
         new_pt = self.blob_next_position(world, vein_pt)
         old_entity = world.get_tile_occupant(new_pt)
         if isinstance(old_entity, entities.Ore):
            old_entity.remove_entity(world)
         return (world.move_entity(self, new_pt), False)


   def create_ore_blob_action(self, world, i_store):
      def action(current_ticks):
         self.remove_pending_action(action)

         entity_pt = self.get_position()
         vein = world.find_nearest(entity_pt, entities.Vein)
         (tiles, found) = self.blob_to_vein(world, vein)

         next_time = current_ticks + self.get_rate()
         if found:
            quake = world.create_quake(tiles[0], current_ticks, i_store)
            world.add_entity(quake)
            next_time = current_ticks + self.get_rate() * 2

         schedule_action(world, self,
            self.create_ore_blob_action(world, i_store),
            next_time)

         return tiles
      return action


   def schedule_entity(self, world, ticks, i_store):
      schedule_action(world, self, self.create_ore_blob_action(world, i_store),
         ticks + self.get_rate())
      schedule_animation(world, self)


class Quake:
   def __init__(self, name, position, imgs, animation_rate):
      self.name = name
      self.position = position
      self.imgs = imgs
      self.current_img = 0
      self.animation_rate = animation_rate
      self.pending_actions = []

   def set_position(self, point):
      self.position = point

   def get_position(self):
      return self.position

   def get_images(self):
      return self.imgs

   def get_image(self):
      return self.imgs[self.current_img]

   def get_rate(self):
      return self.rate

   def get_name(self):
      return self.name

   def get_animation_rate(self):
      return self.animation_rate

   def remove_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.remove(action)

   def add_pending_action(self, action):
      if hasattr(self, "pending_actions"):
         self.pending_actions.append(action)

   def get_pending_actions(self):
      if hasattr(self, "pending_actions"):
         return self.pending_actions
      else:
         return []

   def clear_pending_actions(self):
      if hasattr(self, "pending_actions"):
         self.pending_actions = []

   def next_image(self):
      self.current_img = (self.current_img + 1) % len(self.imgs)

   def entity_string(self):
      return 'unknown'


   def schedule_entity(self, world, ticks):
      schedule_animation(world, self, QUAKE_STEPS) 
      schedule_action(world, self, self.create_entity_death_action(world),
         ticks + QUAKE_DURATION)

   def create_entity_death_action(self, world):
      def action(current_ticks):
         self.remove_pending_action(action)
         pt = self.get_position()
         self.remove_entity(world)
         return [pt]
      return action
      
      
   def remove_entity(self, world):
      for action in self.get_pending_actions():
         world.unschedule_action(action)
      self.clear_pending_actions()
      world.remove_entity(self)
